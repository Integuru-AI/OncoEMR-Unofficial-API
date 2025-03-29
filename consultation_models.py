# models.py
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Literal, Any


# --- FieldContent Definition ---
class FieldContent(BaseModel):
    text: Optional[str] = None
    append: bool = True  # Default append behavior for text fields


# --- Literal Type Definitions ---

# Reused Literals (Define or import these from a shared location if unifying later)
MaritalStatusOptions = Literal["Single", "Married", "Divorced", "Widowed", "Has Significant Other"]
ROSWeightOptions = Literal["No Weight Loss", "Weight Loss"]
ROSFatigueOptions = Literal["No Fatigue", "Fatigue"]
ROSAppetiteOptions = Literal["No Loss of Appetite", "Loss of Appetite"]
ROSNightSweatsOptions = Literal["No night sweats", "Night sweats"]
ROSFeverOptions = Literal["No fever", "Fever"]
ROSChillsOptions = Literal["No Chills", "Chills"]
AssessmentStatusOptions = Literal["NED", "Stable", "Partial Response", "Complete Response", "Progression of Disease"]
ACPLivingWillOptions = Literal["Yes", "No", "Unknown"]
ACPPOAOptions = Literal["Yes", "No", "Unknown"]
ACPPOLSTOptions = Literal["Yes", "No", "Unknown"]
ACPDNROptions = Literal["Yes", "No", "Unknown"]
ACPGoalOfCareOptions = Literal["Palliative", "Curative", "Hospice"]
PainScaleOptions = Literal[
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # Keep for model clarity, mapping ignored
ECOGScaleOptions = Literal["0", "1", "2", "3", "4"]  # Keep for model clarity, mapping ignored

# --- Consultation Specific Literals ---
ConsultationTobaccoStatusOptions = Literal[
    "1 Current Everyday Smoker", "2 Current Some Day Smoker", "3 Former Smoker",
    "4 Never Smoker", "5 Smoker, Current Status Unknown", "9 Unknown If Ever Smoked"
]
ConsultationSmokingCessationOptions = Literal[
    "Not Discussed", "Advised to Quit", "Discussed Cessation Methods", "Discussed Cessation Medications"
]
ConsultationFamilyCancerHistoryOptions = Literal["Yes", "None"]
ConsultationOtherFamilyHistoryOptions = Literal["Other Family History"]  # Single radio option
SHAlcoholUseStatusOptions = Literal["Not Asked", "Never", "Currently uses", "Former use"]
SHDrugUseStatusOptions = Literal["Negative", "Positive"]
YesNoOptions = Literal["Yes", "No"]  # Helper

# ROS Literals
ROSEyesBlurredVisionOptions = Literal["No Blurred Vision", "Blurred Vision"]
ROSEyesDoubleVisionOptions = Literal["No Double Vision", "Double Vision"]
ROSEyesDifficultySeeingOptions = Literal["No difficulty seeing", "Difficulty Seeing"]
ROSENMTHearingLossOptions = Literal["No Hearing Loss", "Hearing Loss"]
ROSENMTRingingOptions = Literal["No Ringing in Ears", "Ringing in Ears"]
ROSENMTSinusOptions = Literal["No Sinus Trouble", "Sinus Trouble"]
ROSENMTSwallowingOptions = Literal["No Trouble Swallowing", "Trouble Swallowing"]
ROSENMTSoreThroatOptions = Literal["No Sore Throat", "Sore Throat"]
ROSENMTDrainageOptions = Literal["No Nasal drainage", "Nasal drainage"]
ROSENMTNoseBleedOptions = Literal["No Nose Bleeds", "Nose Bleeds"]
ROSENMTHoarsenessOptions = Literal["Hoarseness"]
ROSCardiacChestPainOptions = Literal["No Chest Pains", "Chest Pains"]
ROSCardiacPalpitationsOptions = Literal["No Heart Palpitations", "Heart Palpitations"]
ROSCardiacLightheadednessOptions = Literal["No Lightheadedness", "Lightheadedness"]
ROSCardiacSwellingLegsOptions = Literal["No Swelling in Legs", "Swelling in Legs"]
ROSCardiacSyncopeOptions = Literal["No Syncope", "Syncope"]
ROSRespCoughOptions = Literal["No Cough", "Cough"]
ROSRespSputumOptions = Literal["No Sputum Production", "Sputum Production"]
ROSRespHemoptysisOptions = Literal["No Hemoptysis", "Hemoptysis"]
ROSRespSOBOptions = Literal["No Shortness of Breath", "Shortness of Breath"]
ROSRespOrthopneaOptions = Literal["No Orthopnea", "Orthopnea"]
ROSRespNPDOptions = Literal["No Nocturnal Paroxysmal Dyspnea", "Nocturnal Paroxysmal Dyspnea"]
ROSGINauseaOptions = Literal["No Nausea", "Nausea"]
ROSGIVomitingOptions = Literal["No Vomiting", "Vomiting"]
ROSGIHeartburnOptions = Literal["No Heartburn", "Heartburn"]
ROSGIConstipationOptions = Literal["No Constipation", "Constipation"]
ROSGIDiarrheaOptions = Literal["No Diarrhea", "Diarrhea"]
ROSGIAbdominalPainOptions = Literal["No Abdominal Pain", "Abdominal Pain"]
ROSGIRectalBleedingOptions = Literal["No Rectal Bleeding", "Rectal Bleeding"]
ROSGIBowelIncontinenceOptions = Literal["No Bowel Incontinence", "Bowel Incontinence"]
ROSGUBurningOptions = Literal["No Burning on Urination", "Burning on Urination"]
ROSGUPainOptions = Literal["No Pain with Urination", "Pain with Urination"]
ROSGUUrgencyOptions = Literal["No Urgency", "Urgency"]
ROSGUBloodOptions = Literal["No Blood in Urine", "Blood in Urine"]
ROSGUFrequencyOptions = Literal["No Frequent Urination", "Frequent Urination"]
ROSGUIncontinenceOptions = Literal["No Urinary Incontinence", "Urinary Incontinence"]
ROSMSKMusclePainOptions = Literal["No Muscle Pain", "Muscle Pain"]
ROSMSKStiffnessOptions = Literal["No Stiffness", "Stiffness"]
ROSMSKJointPainOptions = Literal["No Joint Pain", "Joint Pain"]
ROSMSKJointSwellingOptions = Literal["No joint swelling", "Joint swelling"]
ROSMSKBackPainOptions = Literal["No Back Pain", "Back Pain"]
ROSSkinStatusOptions = Literal["Not Asked", "No skin rash(es)", "Skin Rash", "Other skin complaints"]
ROSNeuroHeadacheOptions = Literal["No Headaches", "Headaches"]
ROSNeuroSeizureOptions = Literal["No Seizures", "Seizures"]
ROSNeuroDizzinessOptions = Literal["No Dizziness", "Dizziness"]
ROSNeuroBalanceOptions = Literal["No Loss of Balance", "Loss of Balance"]
ROSNeuroWeaknessOptions = Literal["No Weakness of Limbs", "Weakness of Limbs"]
ROSNeuroSensationOptions = Literal["No Loss of Sensation", "Loss of Sensation"]
ROSNeuroTinglingOptions = Literal["No Tingling Sensations", "Tingling Sensations"]
ROSNeuroMemoryOptions = Literal["No Memory Loss", "Memory Loss"]
ROSNeuroThinkingOptions = Literal["No Thinking Difficulty", "Thinking Difficulty"]
ROSPsychStatusOptions = Literal["Deferred", "System"]
ROSPsychNervousnessOptions = Literal["No Nervousness", "Nervousness"]
ROSPsychDepressionOptions = Literal["No Depression", "Depression"]
ROSPsychRestlessnessOptions = Literal["No restlessness", "Restless"]
ROSPsychSleepOptions = Literal["No difficulty sleeping", "Difficulty sleeping"]
ROSHemeBruisingOptions = Literal["No bruising", "Bruising"]
ROSHemeBleedingOptions = Literal["No Bleeding", "Bleeding"]
ROSHemeLumpsArmpitsOptions = Literal["No Lumps in Arm Pits", "Lumps in Arm Pits"]
ROSHemeLumpsNeckOptions = Literal["No Lumps in Neck", "Lumps in Neck"]
ROSHemeLumpsGroinOptions = Literal["No Lumps in Groin", "Lumps in Groin"]

# PE Literals
PEChaperoneOptions = Literal["Accepted", "Declined"]
PEGeneralNutritionOptions = Literal["Well developed, well nourished", "Malnourished/cachectic"]
PEGeneralDistressOptions = Literal["No acute Distress", "Acutely ill-looking", "Chronicly Ill looking"]
PEGeneralAgeAppearanceOptions = Literal["Appears Stated age", "Elderly appearance"]
PEHeadTraumaOptions = Literal["Atraumatic and normocephalic", "Traumatic with a wound/scar on the scalp/face."]
PEEyesPERRLAOptions = Literal["PERRLA", "Unequal"]
PEEyesConjunctivaColorOptions = Literal["Pink palpebral conjunctivae", "Slightly pale palpebral conjunctivae"]
PEEyesEOMOptions = Literal["EOMs intact", "Deviation"]
PEEyesScleraOptions = Literal["No icteric sclera", "Icteric sclera"]
PEEyesConjunctivaClarityOptions = Literal["Conjunctiva Clear", "Conjunctiva red/drainage"]
PEENMTTracheaOptions = Literal["Trachea Midline", "Deviated trachea"]
PEENMTJVDOptions = Literal["NO JVD", "Engorged jugular vessels"]
PEENMTLymphadenopathyOptions = Literal["No Lymphadenopathy", "Lymphadenopathy"]
PEENMTThyroidOptions = Literal["Thyroid Midline-Normal", "Thyroid enlarged/asymmetric"]
PEENMTOralLesionsOptions = Literal["No oral lesions", "Oral abnormality(ies) as noted"]
PECardiacS1S2Options = Literal["S1, S2 no mumurs", "S1, S2 mumurs present."]
PECardiacS3S4Options = Literal["S3,S4 no gallop", "S3/S4 gallop present"]
PECardiacRubsClicksOptions = Literal["No rubs or clicks", "Rub click noted"]
PECardiacBruitsOptions = Literal["No bruits", "Bruits"]
PECardiacRhythmOptions = Literal["Regular heart beat", "Atrial fibrillation"]
PECardiacHeaveOptions = Literal["No parasternal heave", "Parasternal Heave"]
PECardiacRadialPulseOptions = Literal["Radial Pulse Present", "Radial pulses absent"]
PECardiacFemoralPulseOptions = Literal["Femoral Pulses present", "Femoral pulses absent"]
PECardiacPedalPulseOptions = Literal["Pedal Pulses present", "Pedal Pulses absent"]
PERespAuscultationOptions = Literal["Clear, No rales/Rhonchi", "Rales/Rhonchi present", "Pleural Effusion"]
PERespPercussionPalpationOptions = Literal["Percussion and palpation-Normal", "Percussion and palpation abnormal"]
PEGIFirmnessOptions = Literal["Abdomen soft", "Abdomen firmness"]
PEGITendernessOptions = Literal["Abdomen non-tender", "Abdomen Tender"]
PEGIDistensionOptions = Literal["Abdomen non-distended", "Abdomen Distended"]
PEGIMassesOptions = Literal["Abdomen without masses", "Abdomen Mass(es)"]
PEGIAscitesOptions = Literal["No Ascites", "Ascites"]
PEGIHepatomegalyOptions = Literal["No hepatomegaly", "Hepatomegaly"]
PEGISplenomegalyOptions = Literal["No splenomegaly", "Splenomegaly"]
PEGIHerniaOptions = Literal["No hernia", "Hernia"]
PEGIBowelSoundsOptions = Literal["Bowel sounds -Normal", "Bowel sounds -abnormal"]
PEMSKStatusOptions = Literal["Deferred"]
PEMSKGaitOptions = Literal["Normal gait and station", "Abnormal gait and station"]
PEMSKROMOptions = Literal["Range of motion normal", "Decreased range of motion"]
PEMSKToneOptions = Literal["Strength/Tone normal", "Strength/Tone decreased"]
PEMSKStatureOptions = Literal["Stature Normal", "Loss of Stature"]
PEExtremitiesStatusOptions = Literal["Not examined"]
PEExtremitiesEdemaOptions = Literal["Edema-None", "Edema Present"]
PEExtremitiesCyanosisOptions = Literal["Cyanosis-none", "Cyanosis-Present"]
PEExtremitiesClubbingOptions = Literal["Digital Clubbing-None", "Digital clubbing-present"]
PEExtremitiesDiscolorationOptions = Literal["Discoloration-none", "Discoloration-Present"]
PESkinStatusOptions = Literal["System", "Abnormal"]
PENeuroAlertnessOptions = Literal["Alert and Oriented", "Altered orientation/alertness"]
PENeuroSpeechOptions = Literal["Normal Speech", "Abnormal Speech"]
PENeuroHemiplegiaOptions = Literal["No hemiplegia", "Hemiplegia"]
PENeuroHemiparesisOptions = Literal["No hemiparesis", "Hemiparesis"]
PENeuroCranialNervesOptions = Literal["Cranial nerves intact", "Paralysis cranial nerves"]
PENeuroSensoryOptions = Literal["No sensory deficits", "Sensory deficits"]
PENeuroMotorOptions = Literal["No motor deficits", "Motor deficits"]
PERectalOccultBloodOptions = Literal["Occult blood negative", "Occult blood positive"]
PERectalMassesOptions = Literal["No masses", "Mass(es)"]
PEGUProstateOptions = Literal["Prostate Normal", "Prostate Abnormal"]

# MDM Literals
MDMLevelOptions = Literal["High", "Moderate", "Low", "Straightforward"]

ConsultationLengthOfVisitOptions = Literal[
    "Visit length 30 minutes (99203)", "Visit length 44 minutes (99203)",
    "Visit length 45 minutes (99204)", "Visit length 59 minutes (99204)",
    "Visit length 60 minutes (99205)", "Visit length 74 minutes (99205)",
    "Other"
]


# --- Consultation Note Model ---
class ConsultationNoteTemplateModel(BaseModel):
    patient_id: str

    # --- Dx/HPI Section ---
    reason_for_consult: FieldContent = Field(default_factory=FieldContent)
    disease_history: FieldContent = Field(default_factory=FieldContent)
    interim_history: FieldContent = Field(default_factory=FieldContent)
    # Grid placeholders (Content ignored by standard mapping)
    oncology_diagnoses_grid: Optional[List[Any]] = None
    assessed_problems_grid: Optional[List[Any]] = None
    secondary_problems_grid: Optional[List[Any]] = None
    # Assessment status dictionaries (Specific keys ignored by standard mapping)
    assessed_oncology_diagnoses: Dict[str, bool] = Field(default_factory=dict)
    assessed_other_diagnoses: Dict[str, bool] = Field(default_factory=dict)
    assessed_secondary_problems: Dict[str, bool] = Field(default_factory=dict)

    # --- PMH/Surg Hx Section ---
    past_medical_history: FieldContent = Field(default_factory=FieldContent)
    past_surgical_history: FieldContent = Field(default_factory=FieldContent)
    hm_colonoscopy_enabled: Optional[bool] = None
    hm_colonoscopy_details: FieldContent = Field(default_factory=FieldContent)
    hm_dexascan_enabled: Optional[bool] = None
    hm_dexascan_details: FieldContent = Field(default_factory=FieldContent)

    # --- SH/FH Section ---
    marital_status: Optional[MaritalStatusOptions] = None
    sh_living_with_spouse: Optional[bool] = None
    sh_living_alone: Optional[bool] = None
    sh_living_with_children: Optional[bool] = None
    sh_living_nursing_home: Optional[bool] = None
    sh_living_other_enabled: Optional[bool] = None
    sh_living_arrangements_other_details: FieldContent = Field(default_factory=FieldContent)
    tobacco_status: Optional[ConsultationTobaccoStatusOptions] = None
    smoking_cessation: Optional[ConsultationSmokingCessationOptions] = None
    sh_tobacco_discontinued_year_enabled: Optional[bool] = None
    sh_tobacco_discontinued_year: FieldContent = Field(default_factory=FieldContent)
    sh_tobacco_pack_years_enabled: Optional[bool] = None
    sh_tobacco_pack_years: FieldContent = Field(default_factory=FieldContent)
    sh_tobacco_type_details_enabled: Optional[bool] = None
    sh_tobacco_type_details: FieldContent = Field(default_factory=FieldContent)
    sh_alcohol_use_status: Optional[SHAlcoholUseStatusOptions] = None
    sh_alcohol_drinks_per_day_enabled: Optional[bool] = None
    sh_alcohol_drinks_per_day: FieldContent = Field(default_factory=FieldContent)
    sh_alcohol_drinks_per_week_enabled: Optional[bool] = None
    sh_alcohol_drinks_per_week: FieldContent = Field(default_factory=FieldContent)
    sh_alcohol_drinks_per_month_enabled: Optional[bool] = None
    sh_alcohol_drinks_per_month: FieldContent = Field(default_factory=FieldContent)
    sh_alcohol_drinks_per_year_enabled: Optional[bool] = None
    sh_alcohol_drinks_per_year: FieldContent = Field(default_factory=FieldContent)
    sh_alcohol_stopped_year_enabled: Optional[bool] = None
    sh_alcohol_stopped_year: FieldContent = Field(default_factory=FieldContent)
    sh_drug_use_status: Optional[SHDrugUseStatusOptions] = None
    sh_drug_use_type_enabled: Optional[bool] = None
    sh_drug_use_type_details: FieldContent = Field(default_factory=FieldContent)
    primary_occupation: FieldContent = Field(default_factory=FieldContent)
    secondary_occupation: FieldContent = Field(default_factory=FieldContent)
    sh_occupational_exposure_none: Optional[bool] = None
    sh_occupational_exposure_type_enabled: Optional[bool] = None
    sh_occupational_exposure_type_details: FieldContent = Field(default_factory=FieldContent)
    sh_occupational_exposure_solvent: Optional[bool] = None
    sh_occupational_exposure_asbestos: Optional[bool] = None
    sh_occupational_exposure_agent_orange: Optional[bool] = None
    family_history_grid: Optional[List[Any]] = None  # Content ignored by mapping
    family_history_comment: FieldContent = Field(default_factory=FieldContent)
    mother_cancer_history: Optional[ConsultationFamilyCancerHistoryOptions] = None
    mother_cancer_history_details: FieldContent = Field(default_factory=FieldContent)
    father_cancer_history: Optional[ConsultationFamilyCancerHistoryOptions] = None
    father_cancer_history_details: FieldContent = Field(default_factory=FieldContent)
    siblings_cancer_history: Optional[ConsultationFamilyCancerHistoryOptions] = None
    siblings_cancer_history_details: FieldContent = Field(default_factory=FieldContent)
    children_cancer_history: Optional[ConsultationFamilyCancerHistoryOptions] = None
    children_cancer_history_details: FieldContent = Field(default_factory=FieldContent)
    other_family_history_status: Optional[ConsultationOtherFamilyHistoryOptions] = None
    other_family_history_details: FieldContent = Field(default_factory=FieldContent)

    # --- Allergies/Meds Section (Placeholder - Ignored by standard mapping) ---
    # allergies_summary: Optional[str] = None
    # medications_summary: Optional[str] = None

    # --- ROS Section ---
    review_of_systems: FieldContent = Field(default_factory=FieldContent)
    ros_general_system_negative: Optional[bool] = None
    ros_weight: Optional[ROSWeightOptions] = None
    ros_weight_loss_details: FieldContent = Field(default_factory=FieldContent)
    ros_fatigue: Optional[ROSFatigueOptions] = None
    ros_appetite: Optional[ROSAppetiteOptions] = None
    ros_night_sweats: Optional[ROSNightSweatsOptions] = None
    ros_fever: Optional[ROSFeverOptions] = None
    ros_chills: Optional[ROSChillsOptions] = None

    ros_eyes_system_negative: Optional[bool] = None
    ros_eyes_blurred_vision: Optional[ROSEyesBlurredVisionOptions] = None
    ros_eyes_double_vision: Optional[ROSEyesDoubleVisionOptions] = None
    ros_eyes_difficulty_seeing: Optional[ROSEyesDifficultySeeingOptions] = None

    ros_enmt_system_negative: Optional[bool] = None
    ros_enmt_hearing_loss: Optional[ROSENMTHearingLossOptions] = None
    ros_enmt_ringing_ears: Optional[ROSENMTRingingOptions] = None
    ros_enmt_sinus_trouble: Optional[ROSENMTSinusOptions] = None
    ros_enmt_trouble_swallowing: Optional[ROSENMTSwallowingOptions] = None
    ros_enmt_sore_throat: Optional[ROSENMTSoreThroatOptions] = None
    ros_enmt_nasal_drainage: Optional[ROSENMTDrainageOptions] = None
    ros_nasal_drainage_details: FieldContent = Field(default_factory=FieldContent)
    ros_enmt_nose_bleeds: Optional[ROSENMTNoseBleedOptions] = None
    ros_enmt_hoarseness: Optional[ROSENMTHoarsenessOptions] = None

    ros_cardiac_system_negative: Optional[bool] = None
    ros_cardiac_chest_pain: Optional[ROSCardiacChestPainOptions] = None
    ros_cardiac_palpitations: Optional[ROSCardiacPalpitationsOptions] = None
    ros_cardiac_lightheadedness: Optional[ROSCardiacLightheadednessOptions] = None
    ros_cardiac_swelling_legs: Optional[ROSCardiacSwellingLegsOptions] = None
    ros_cardiac_syncope: Optional[ROSCardiacSyncopeOptions] = None
    ros_cardiac_raynauds_no: Optional[bool] = None  # Corrected from Literal
    ros_cardiac_raynauds_yes: Optional[bool] = None  # Corrected from Literal

    ros_resp_system_negative: Optional[bool] = None
    ros_resp_cough: Optional[ROSRespCoughOptions] = None
    ros_resp_sputum: Optional[ROSRespSputumOptions] = None
    ros_resp_hemoptysis: Optional[ROSRespHemoptysisOptions] = None
    ros_resp_sob: Optional[ROSRespSOBOptions] = None
    ros_resp_orthopnea: Optional[ROSRespOrthopneaOptions] = None
    ros_resp_npd: Optional[ROSRespNPDOptions] = None

    ros_gi_system_negative: Optional[bool] = None
    ros_gi_nausea: Optional[ROSGINauseaOptions] = None
    ros_gi_vomiting: Optional[ROSGIVomitingOptions] = None
    ros_gi_heartburn: Optional[ROSGIHeartburnOptions] = None
    ros_gi_constipation: Optional[ROSGIConstipationOptions] = None
    ros_gi_diarrhea: Optional[ROSGIDiarrheaOptions] = None
    ros_gi_abdominal_pain: Optional[ROSGIAbdominalPainOptions] = None
    ros_gi_rectal_bleeding: Optional[ROSGIRectalBleedingOptions] = None
    ros_gi_bowel_incontinence: Optional[ROSGIBowelIncontinenceOptions] = None

    ros_gu_system_negative: Optional[bool] = None
    ros_gu_burning_urination: Optional[ROSGUBurningOptions] = None
    ros_gu_pain_urination: Optional[ROSGUPainOptions] = None
    ros_gu_urgency: Optional[ROSGUUrgencyOptions] = None
    ros_gu_blood_urine: Optional[ROSGUBloodOptions] = None
    ros_gu_frequent_urination: Optional[ROSGUFrequencyOptions] = None
    ros_gu_urinary_incontinence: Optional[ROSGUIncontinenceOptions] = None

    ros_msk_system_negative: Optional[bool] = None
    ros_msk_muscle_pain: Optional[ROSMSKMusclePainOptions] = None
    ros_msk_stiffness: Optional[ROSMSKStiffnessOptions] = None
    ros_msk_joint_pain: Optional[ROSMSKJointPainOptions] = None
    ros_msk_joint_swelling: Optional[ROSMSKJointSwellingOptions] = None
    ros_msk_back_pain: Optional[ROSMSKBackPainOptions] = None

    ros_skin_status: Optional[ROSSkinStatusOptions] = None
    ros_skin_other_details: FieldContent = Field(default_factory=FieldContent)

    ros_neuro_system_negative: Optional[bool] = None
    ros_neuro_headaches: Optional[ROSNeuroHeadacheOptions] = None
    ros_neuro_seizures: Optional[ROSNeuroSeizureOptions] = None
    ros_neuro_dizziness: Optional[ROSNeuroDizzinessOptions] = None
    ros_neuro_loss_of_balance: Optional[ROSNeuroBalanceOptions] = None
    ros_neuro_weakness_limbs: Optional[ROSNeuroWeaknessOptions] = None
    ros_neuro_loss_of_sensation: Optional[ROSNeuroSensationOptions] = None
    ros_neuro_tingling: Optional[ROSNeuroTinglingOptions] = None
    ros_neuro_memory_loss: Optional[ROSNeuroMemoryOptions] = None
    ros_neuro_thinking_difficulty: Optional[ROSNeuroThinkingOptions] = None

    ros_psych_status: Optional[ROSPsychStatusOptions] = None
    ros_psych_nervousness: Optional[ROSPsychNervousnessOptions] = None
    ros_psych_depression: Optional[ROSPsychDepressionOptions] = None
    ros_psych_restlessness: Optional[ROSPsychRestlessnessOptions] = None
    ros_psych_difficulty_sleeping: Optional[ROSPsychSleepOptions] = None

    ros_heme_system_negative: Optional[bool] = None
    ros_heme_bruising: Optional[ROSHemeBruisingOptions] = None
    ros_heme_bleeding: Optional[ROSHemeBleedingOptions] = None
    ros_heme_bleeding_details: FieldContent = Field(default_factory=FieldContent)
    ros_heme_lumps_armpits: Optional[ROSHemeLumpsArmpitsOptions] = None
    ros_heme_lumps_neck: Optional[ROSHemeLumpsNeckOptions] = None
    ros_heme_lumps_groin: Optional[ROSHemeLumpsGroinOptions] = None

    ros_endo_system_negative: Optional[bool] = None  # FD_chkHLI
    ros_endo_no_polydipsia: Optional[bool] = None  # FD_chkROSEndo_NP (Corrected)
    ros_endo_polydipsia_present: Optional[bool] = None  # FD_chkROSEndo_Polydipsia (Corrected)
    ros_endo_no_polyphagia: Optional[bool] = None  # FD_chkROSEndo_NoP (Corrected)
    ros_endo_polyphagia_present: Optional[bool] = None  # FD_chkROSEndo_Polyphagia (Corrected)
    ros_endo_no_polyuria: Optional[bool] = None  # FD_chkROSEndo_NoPolyuria (Corrected)
    ros_endo_polyuria_present: Optional[bool] = None  # FD_chkROSEndo_Polyuria (Corrected)

    # --- PAIN/DEPRESSION Section ---
    pain_scale_score: Optional[PainScaleOptions] = None  # Value ignored by standard mapping
    pain_tx_reassess: Optional[bool] = None
    pain_tx_continue: Optional[bool] = None
    pain_tx_narcotic_adjusted: Optional[bool] = None
    pain_tx_narcotic_prescribed: Optional[bool] = None
    pain_tx_non_narcotic_adjusted: Optional[bool] = None
    pain_tx_non_narcotic_prescribed: Optional[bool] = None
    pain_tx_psych_support: Optional[bool] = None
    pain_tx_education: Optional[bool] = None
    pain_tx_refer_pain_mgmt: Optional[bool] = None
    pain_tx_refused: Optional[bool] = None
    pain_tx_other_provider: Optional[bool] = None
    depression_screening_phq9: Optional[str] = None  # Value ignored by standard mapping
    physician_note_on_depression_score: FieldContent = Field(default_factory=FieldContent)
    depression_tx_no_action: Optional[bool] = None
    depression_tx_psychotherapy: Optional[bool] = None
    depression_tx_meds_prescribed: Optional[bool] = None
    depression_tx_declined_meds: Optional[bool] = None
    depression_tx_declined_referral: Optional[bool] = None
    depression_tx_other_provider: Optional[bool] = None
    depression_tx_refused: Optional[bool] = None
    depression_tx_inaccurate_screen: Optional[bool] = None
    depression_tx_bipolar_excluded: Optional[bool] = None

    # --- PE Section ---
    physical_exam: FieldContent = Field(default_factory=FieldContent)
    pe_chaperone_status: Optional[PEChaperoneOptions] = None
    pe_general_system_negative: Optional[bool] = None
    pe_general_nutrition: Optional[PEGeneralNutritionOptions] = None
    pe_general_distress: Optional[PEGeneralDistressOptions] = None
    ecog_performance_score: Optional[ECOGScaleOptions] = None  # Value ignored by standard mapping
    pe_general_age_appearance: Optional[PEGeneralAgeAppearanceOptions] = None
    pe_head_system_negative: Optional[bool] = None
    pe_head_trauma: Optional[PEHeadTraumaOptions] = None
    pe_eyes_system_negative: Optional[bool] = None
    pe_eyes_deferred: Optional[bool] = None
    pe_eyes_perrla: Optional[PEEyesPERRLAOptions] = None
    pe_eyes_conjunctiva_color: Optional[PEEyesConjunctivaColorOptions] = None
    pe_eyes_eom: Optional[PEEyesEOMOptions] = None
    pe_eyes_sclera: Optional[PEEyesScleraOptions] = None
    pe_eyes_conjunctiva_clarity: Optional[PEEyesConjunctivaClarityOptions] = None
    pe_enmt_system_negative: Optional[bool] = None
    pe_enmt_trachea: Optional[PEENMTTracheaOptions] = None
    pe_enmt_jvd: Optional[PEENMTJVDOptions] = None
    pe_enmt_lymphadenopathy: Optional[PEENMTLymphadenopathyOptions] = None
    pe_lymphadenopathy_details: FieldContent = Field(default_factory=FieldContent)
    pe_enmt_thyroid: Optional[PEENMTThyroidOptions] = None
    pe_enmt_nodes_present: Optional[bool] = None
    pe_enmt_oral_lesions: Optional[PEENMTOralLesionsOptions] = None
    pe_oral_abnormality_details: FieldContent = Field(default_factory=FieldContent)
    pe_enmt_tracheostomy_present: Optional[bool] = None
    pe_cardiac_system_negative: Optional[bool] = None
    pe_cardiac_s1s2: Optional[PECardiacS1S2Options] = None
    pe_cardiac_s3s4: Optional[PECardiacS3S4Options] = None
    pe_cardiac_rubs_clicks: Optional[PECardiacRubsClicksOptions] = None
    pe_cardiac_bruits: Optional[PECardiacBruitsOptions] = None
    pe_cardiac_rhythm: Optional[PECardiacRhythmOptions] = None
    pe_cardiac_heave: Optional[PECardiacHeaveOptions] = None
    pe_cardiac_radial_pulse: Optional[PECardiacRadialPulseOptions] = None
    pe_cardiac_femoral_pulse: Optional[PECardiacFemoralPulseOptions] = None
    pe_cardiac_pedal_pulse: Optional[PECardiacPedalPulseOptions] = None
    pe_resp_system_negative: Optional[bool] = None
    pe_resp_auscultation: Optional[PERespAuscultationOptions] = None
    pe_resp_percussion_palpation: Optional[PERespPercussionPalpationOptions] = None
    pe_respiratory_also_noted_enabled: Optional[bool] = None
    pe_respiratory_also_noted_details: FieldContent = Field(default_factory=FieldContent)
    pe_gi_system_negative: Optional[bool] = None
    pe_abdomen_scars_enabled: Optional[bool] = None
    pe_abdomen_scars_details: FieldContent = Field(default_factory=FieldContent)
    pe_gi_firmness: Optional[PEGIFirmnessOptions] = None
    pe_gi_tenderness: Optional[PEGITendernessOptions] = None
    pe_gi_distension: Optional[PEGIDistensionOptions] = None
    pe_gi_masses: Optional[PEGIMassesOptions] = None
    pe_gi_ascites: Optional[PEGIAscitesOptions] = None
    pe_gi_hepatomegaly: Optional[PEGIHepatomegalyOptions] = None
    pe_gi_splenomegaly: Optional[PEGISplenomegalyOptions] = None
    pe_gi_ostomy_present: Optional[bool] = None
    pe_gi_hernia: Optional[PEGIHerniaOptions] = None
    pe_gi_bowel_sounds: Optional[PEGIBowelSoundsOptions] = None
    pe_heme_system_negative: Optional[bool] = None
    pe_heme_petechiae_no: Optional[bool] = None  # Corrected
    pe_heme_petechiae_yes: Optional[bool] = None  # Corrected
    pe_heme_purpura_no: Optional[bool] = None  # Corrected
    pe_heme_purpura_yes: Optional[bool] = None  # Corrected
    pe_heme_neck_lymph_no: Optional[bool] = None  # Corrected
    pe_heme_neck_lymph_yes: Optional[bool] = None  # Corrected
    pe_heme_axillary_lymph_no: Optional[bool] = None  # Corrected
    pe_heme_axillary_lymph_yes: Optional[bool] = None  # Corrected
    pe_heme_groin_lymph_no: Optional[bool] = None  # Corrected
    pe_heme_groin_lymph_yes: Optional[bool] = None  # Corrected
    pe_msk_system_negative: Optional[bool] = None
    pe_msk_deferred: Optional[bool] = None  # Correction: Was PEMSKStatusOptions before
    pe_msk_gait: Optional[PEMSKGaitOptions] = None
    pe_msk_rom: Optional[PEMSKROMOptions] = None
    pe_msk_tone: Optional[PEMSKToneOptions] = None
    pe_msk_stature: Optional[PEMSKStatureOptions] = None
    pe_msk_also_noted_enabled: Optional[bool] = None
    pe_msk_also_noted_details: FieldContent = Field(default_factory=FieldContent)
    pe_extremities_system_negative: Optional[bool] = None
    pe_extremities_status: Optional[PEExtremitiesStatusOptions] = None
    pe_extremities_edema: Optional[PEExtremitiesEdemaOptions] = None
    pe_edema_details: FieldContent = Field(default_factory=FieldContent)
    pe_extremities_cyanosis: Optional[PEExtremitiesCyanosisOptions] = None
    pe_extremities_clubbing: Optional[PEExtremitiesClubbingOptions] = None
    pe_extremities_discoloration: Optional[PEExtremitiesDiscolorationOptions] = None
    pe_skin_status: Optional[PESkinStatusOptions] = None
    pe_neuro_system_negative: Optional[bool] = None
    pe_neuro_alertness: Optional[PENeuroAlertnessOptions] = None
    pe_neuro_speech: Optional[PENeuroSpeechOptions] = None
    pe_abnormal_speech_details: FieldContent = Field(default_factory=FieldContent)
    pe_neuro_hemiplegia: Optional[PENeuroHemiplegiaOptions] = None
    pe_neuro_hemiparesis: Optional[PENeuroHemiparesisOptions] = None
    pe_neuro_cranial_nerves: Optional[PENeuroCranialNervesOptions] = None
    pe_neuro_sensory: Optional[PENeuroSensoryOptions] = None
    pe_neuro_motor: Optional[PENeuroMotorOptions] = None
    pe_rectal_system_negative: Optional[bool] = None
    pe_rectal_deferred: Optional[bool] = None
    pe_rectal_occult_blood: Optional[PERectalOccultBloodOptions] = None
    pe_rectal_masses: Optional[PERectalMassesOptions] = None
    pe_gu_system_negative: Optional[bool] = None
    pe_gu_deferred: Optional[bool] = None
    pe_gu_prostate: Optional[PEGUProstateOptions] = None

    # --- Lab/Test Results ---
    peripheral_smear_normal: Optional[bool] = None
    peripheral_smear_micro: Optional[bool] = None
    peripheral_smear_macro: Optional[bool] = None
    peripheral_smear_comment: FieldContent = Field(default_factory=FieldContent)
    other_lab_studies: FieldContent = Field(default_factory=FieldContent)
    radiology_results: FieldContent = Field(default_factory=FieldContent)

    # --- Assessment/Plan ---
    assessment_status: Optional[AssessmentStatusOptions] = None
    assessment: FieldContent = Field(default_factory=FieldContent)
    acp_date_of_discussion_enabled: Optional[bool] = None
    acp_date_of_discussion_details: FieldContent = Field(default_factory=FieldContent)
    acp_living_will: Optional[ACPLivingWillOptions] = None
    acp_poa: Optional[ACPPOAOptions] = None
    acp_polst: Optional[ACPPOLSTOptions] = None
    acp_dnr: Optional[ACPDNROptions] = None
    acp_goal_of_care: Optional[ACPGoalOfCareOptions] = None
    plan: FieldContent = Field(default_factory=FieldContent)

    # --- Time Spent ---
    length_of_patient_visit: Optional[ConsultationLengthOfVisitOptions] = None
    length_of_patient_visit_other_minutes: FieldContent = Field(default_factory=FieldContent)

    # --- MDM ---
    mdm_level: Optional[MDMLevelOptions] = None
    mdm_high_numcomplex_chronic_severe: Optional[bool] = None
    mdm_high_numcomplex_threat_to_life: Optional[bool] = None
    mdm_moderate_numcomplex_chronic_exacerbation: Optional[bool] = None
    mdm_moderate_numcomplex_stable_chronic: Optional[bool] = None
    mdm_moderate_numcomplex_undiagnosed_uncertain: Optional[bool] = None
    mdm_moderate_numcomplex_acute_systemic: Optional[bool] = None
    mdm_moderate_numcomplex_acute_complicated: Optional[bool] = None
    mdm_low_numcomplex_self_limited_minor: Optional[bool] = None
    mdm_low_numcomplex_stable_chronic: Optional[bool] = None
    mdm_low_numcomplex_acute_uncomplicated: Optional[bool] = None
    mdm_high_cat1_review_notes: Optional[bool] = None
    mdm_high_cat1_review_test: Optional[bool] = None
    mdm_high_cat1_order_test: Optional[bool] = None
    mdm_high_cat1_independent_historian: Optional[bool] = None
    mdm_high_cat2_independent_interpretation: Optional[bool] = None
    mdm_high_cat3_discussion: Optional[bool] = None
    mdm_moderate_cat1_review_notes: Optional[bool] = None
    mdm_moderate_cat1_review_test: Optional[bool] = None
    mdm_moderate_cat1_order_test: Optional[bool] = None
    mdm_moderate_cat1_independent_historian: Optional[bool] = None
    mdm_moderate_cat2_independent_interpretation: Optional[bool] = None
    mdm_moderate_cat3_discussion: Optional[bool] = None
    mdm_low_amount_tests_docs: Optional[bool] = None
    mdm_low_amount_independent_historian: Optional[bool] = None
    mdm_high_risk_drug_monitoring: Optional[bool] = None
    mdm_high_risk_elective_major_surgery_risks: Optional[bool] = None
    mdm_high_risk_hospitalization: Optional[bool] = None
    mdm_high_risk_dnr_deescalate: Optional[bool] = None
    mdm_moderate_risk_rx_mgmt: Optional[bool] = None
    mdm_moderate_risk_minor_surgery_risks: Optional[bool] = None
    mdm_moderate_risk_elective_major_surgery_no_risks: Optional[bool] = None
    mdm_moderate_risk_social_determinants: Optional[bool] = None
    mdm_low_risk: Optional[bool] = None
    pe_chest_also_noted_enabled: Optional[bool] = None

    class Config:
        extra = 'ignore'  # Ignore fields from input not defined in the model
