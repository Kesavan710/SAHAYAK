"""
Shared enumerations for the RPwD application feature.
All team members must use these exact values — do not redefine locally.
"""

from enum import Enum


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    COLLECTING_INFORMATION = "collecting_information"
    READY_FOR_REVIEW = "ready_for_review"
    CONFIRMED = "confirmed"
    PDF_GENERATED = "pdf_generated"
    ERROR = "error"


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"


class OnsetType(str, Enum):
    FROM_BIRTH = "from_birth"
    SINCE_YEAR = "since_year"


class EducationalStatus(str, Enum):
    NO_FORMAL_EDUCATION = "No Formal Education"
    PRIMARY = "Primary (up to Class 5)"
    UPPER_PRIMARY = "Upper Primary (up to Class 8)"
    SECONDARY = "Secondary (Class 10 / SSLC)"
    HIGHER_SECONDARY = "Higher Secondary (Class 12 / PUC)"
    DIPLOMA = "Diploma"
    GRADUATE = "Graduate"
    POST_GRADUATE = "Post Graduate"
    DOCTORATE = "Doctorate"


class OccupationType(str, Enum):
    STUDENT = "Student"
    EMPLOYED = "Employed"
    SELF_EMPLOYED = "Self-Employed"
    UNEMPLOYED = "Unemployed"
    HOMEMAKER = "Homemaker"
    RETIRED = "Retired"
    OTHER = "Other"


class DisabilityType(str, Enum):
    VISUAL = "Visual Impairment"
    HEARING = "Hearing Impairment"
    SPEECH_LANGUAGE = "Speech and Language Disability"
    LOCOMOTOR = "Locomotor Disability"
    INTELLECTUAL = "Intellectual Disability"
    MENTAL_ILLNESS = "Mental Illness"
    AUTISM = "Autism Spectrum Disorder"
    CEREBRAL_PALSY = "Cerebral Palsy"
    SPECIFIC_LEARNING = "Specific Learning Disability"
    MULTIPLE = "Multiple Disabilities"
    OTHER = "Other"


# Normalisation map: accepts common natural-language inputs → canonical DisabilityType value
DISABILITY_TYPE_NORMALISE = {
    "blind": DisabilityType.VISUAL,
    "visually impaired": DisabilityType.VISUAL,
    "low vision": DisabilityType.VISUAL,
    "visual": DisabilityType.VISUAL,
    "deaf": DisabilityType.HEARING,
    "hard of hearing": DisabilityType.HEARING,
    "hearing": DisabilityType.HEARING,
    "hearing impairment": DisabilityType.HEARING,
    "mute": DisabilityType.SPEECH_LANGUAGE,
    "speech": DisabilityType.SPEECH_LANGUAGE,
    "locomotor": DisabilityType.LOCOMOTOR,
    "ortho": DisabilityType.LOCOMOTOR,
    "orthopedic": DisabilityType.LOCOMOTOR,
    "physical": DisabilityType.LOCOMOTOR,
    "intellectual": DisabilityType.INTELLECTUAL,
    "mental retardation": DisabilityType.INTELLECTUAL,
    "cognitive": DisabilityType.INTELLECTUAL,
    "mental illness": DisabilityType.MENTAL_ILLNESS,
    "psychiatric": DisabilityType.MENTAL_ILLNESS,
    "autism": DisabilityType.AUTISM,
    "asd": DisabilityType.AUTISM,
    "cerebral palsy": DisabilityType.CEREBRAL_PALSY,
    "cp": DisabilityType.CEREBRAL_PALSY,
    "dyslexia": DisabilityType.SPECIFIC_LEARNING,
    "specific learning": DisabilityType.SPECIFIC_LEARNING,
    "multiple": DisabilityType.MULTIPLE,
    "multiple disabilities": DisabilityType.MULTIPLE,
}


# Normalisation map: gender inputs → canonical Gender value
GENDER_NORMALISE = {
    "male": Gender.MALE, "m": Gender.MALE, "man": Gender.MALE, "boy": Gender.MALE,
    "female": Gender.FEMALE, "f": Gender.FEMALE, "woman": Gender.FEMALE, "girl": Gender.FEMALE,
    "transgender": Gender.TRANSGENDER, "trans": Gender.TRANSGENDER,
    "other": Gender.OTHER,
}


# Normalisation map: education inputs → canonical EducationalStatus value
EDUCATION_NORMALISE = {
    "no education": EducationalStatus.NO_FORMAL_EDUCATION,
    "illiterate": EducationalStatus.NO_FORMAL_EDUCATION,
    "primary": EducationalStatus.PRIMARY,
    "class 5": EducationalStatus.PRIMARY,
    "upper primary": EducationalStatus.UPPER_PRIMARY,
    "class 8": EducationalStatus.UPPER_PRIMARY,
    "sslc": EducationalStatus.SECONDARY,
    "class 10": EducationalStatus.SECONDARY,
    "10th": EducationalStatus.SECONDARY,
    "secondary": EducationalStatus.SECONDARY,
    "puc": EducationalStatus.HIGHER_SECONDARY,
    "class 12": EducationalStatus.HIGHER_SECONDARY,
    "12th": EducationalStatus.HIGHER_SECONDARY,
    "higher secondary": EducationalStatus.HIGHER_SECONDARY,
    "hsc": EducationalStatus.HIGHER_SECONDARY,
    "diploma": EducationalStatus.DIPLOMA,
    "ug": EducationalStatus.GRADUATE,
    "graduate": EducationalStatus.GRADUATE,
    "degree": EducationalStatus.GRADUATE,
    "bsc": EducationalStatus.GRADUATE,
    "ba": EducationalStatus.GRADUATE,
    "bcom": EducationalStatus.GRADUATE,
    "be": EducationalStatus.GRADUATE,
    "btech": EducationalStatus.GRADUATE,
    "undergraduate": EducationalStatus.GRADUATE,
    "pg": EducationalStatus.POST_GRADUATE,
    "post graduate": EducationalStatus.POST_GRADUATE,
    "postgraduate": EducationalStatus.POST_GRADUATE,
    "masters": EducationalStatus.POST_GRADUATE,
    "msc": EducationalStatus.POST_GRADUATE,
    "mtech": EducationalStatus.POST_GRADUATE,
    "phd": EducationalStatus.DOCTORATE,
    "doctorate": EducationalStatus.DOCTORATE,
}
