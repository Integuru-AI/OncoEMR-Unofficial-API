from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Literal


class FieldContent(BaseModel):
    text: Optional[str] = None
    append: bool = True


class CatchAllModel(BaseModel):
    note_name: str
    patient_id: str
    chief_complaint: FieldContent = Field(default_factory=FieldContent)
    disease_history: FieldContent = Field(default_factory=FieldContent)
    interim_history: FieldContent = Field(default_factory=FieldContent)
    past_medical_history: FieldContent = Field(default_factory=FieldContent)
    past_surgical_history: FieldContent = Field(default_factory=FieldContent)
    primary_occupation: FieldContent = Field(default_factory=FieldContent)
    secondary_occupation: FieldContent = Field(default_factory=FieldContent)
    review_of_systems: FieldContent = Field(default_factory=FieldContent)
    physician_note_on_depression_score: FieldContent = Field(
        default_factory=FieldContent
    )
    physical_exam: FieldContent = Field(default_factory=FieldContent)
    other_lab_studies: FieldContent = Field(default_factory=FieldContent)
    radiology_results: FieldContent = Field(default_factory=FieldContent)
    assessment: FieldContent = Field(default_factory=FieldContent)
    plan: FieldContent = Field(default_factory=FieldContent)


GENERIC_TEXTFIELDS_MAPPING = {
    "chief_complaint": "FD_txtDHVT_Reasonforconsult",
    "disease_history": "FD_txtTreatment History",
    "interim_history": "FD_txtHPIT",
    "past_medical_history": "FD_txtPastMedicalHistory",
    "past_surgical_history": "FD_txtPFSHSurgical",
    "primary_occupation": "FD_txtPFSHPrimOcc",
    "secondary_occupation": "FD_txtPFSHSecOcc",
    "review_of_systems": "FD_txtallnormalROS",
    "physician_note_on_depression_score": "FD_txtPhysicianNoteonDepressionScore",
    "physical_exam": "FD_txtallnormal2",
    "other_lab_studies": "FD_txtOLS",
    "radiology_results": "FD_txtRadiologyResults",
    "assessment": "FD_txtDiagnosis",
    "plan": "FD_txtIP_Plan",
    # Add mappings for other fields
    # If some fields don't have a direct mapping, you can handle them separately
}
