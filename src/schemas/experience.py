from pydantic import BaseModel

class Experience(BaseModel):
    role: str
    company: str
    country: str
    startDate: str
    endDate: str
    responsibilities: list[str]
    technologies: list[str]
    isCurrent: bool = False

class ExperienceResponse(Experience):
    id: str