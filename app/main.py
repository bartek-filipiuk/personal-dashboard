from datetime import datetime, timedelta
from typing import Optional
import re

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import Boolean, DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

app = FastAPI(title="Personal Dashboard")
templates = Jinja2Templates(directory="templates")


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    all_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


engine = create_engine("sqlite:///./dashboard.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    start: datetime
    end: Optional[datetime] = None
    all_day: bool = False
    notes: Optional[str] = Field(default=None, max_length=5000)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_range(self):
        if self.end and self.end < self.start:
            raise ValueError("end must be >= start")
        return self


class EventUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    all_day: Optional[bool] = None
    notes: Optional[str] = Field(default=None, max_length=5000)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("title cannot be empty")
        return value


class EventOut(BaseModel):
    id: int
    title: str
    start: datetime
    end: Optional[datetime]
    all_day: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


class QuickAddIn(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("quick-add text cannot be empty")
        return value


def parse_quick_add(text: str) -> EventCreate:
    text = text.strip()

    # Supported formats:
    # - "Title YYYY-MM-DD HH:MM"
    # - "Title YYYY-MM-DDTHH:MM"
    # - "Title jutro HH:MM"
    m_iso = re.match(
        r"^(?P<title>.+?)\s+(?P<date>\d{4}-\d{2}-\d{2})[T\s](?P<time>\d{1,2}:\d{2})$",
        text,
    )
    if m_iso:
        title = m_iso.group("title").strip()
        start = datetime.strptime(f"{m_iso.group('date')} {m_iso.group('time')}", "%Y-%m-%d %H:%M")
        return EventCreate(title=title, start=start)

    m_tomorrow = re.match(r"^(?P<title>.+?)\s+jutro\s+(?P<time>\d{1,2}:\d{2})$", text, re.IGNORECASE)
    if m_tomorrow:
        title = m_tomorrow.group("title").strip()
        t = datetime.strptime(m_tomorrow.group("time"), "%H:%M").time()
        start = datetime.combine((datetime.utcnow() + timedelta(days=1)).date(), t)
        return EventCreate(title=title, start=start)

    raise ValueError(
        "unsupported format. Use: 'Title YYYY-MM-DD HH:MM', 'Title YYYY-MM-DDTHH:MM' or 'Title jutro HH:MM'"
    )


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/events", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    rows = db.execute(select(Event).order_by(Event.start.asc())).scalars().all()
    return rows


@app.get("/api/events/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="event not found")
    return ev


@app.post("/api/events", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    ev = Event(**payload.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@app.put("/api/events/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db)):
    ev = db.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="event not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(ev, k, v)

    if ev.end and ev.end < ev.start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@app.delete("/api/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="event not found")
    db.delete(ev)
    db.commit()
    return {"ok": True}


@app.post("/api/events/quick-add", response_model=EventOut, status_code=201)
def quick_add(payload: QuickAddIn, db: Session = Depends(get_db)):
    try:
        parsed = parse_quick_add(payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    ev = Event(**parsed.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev
