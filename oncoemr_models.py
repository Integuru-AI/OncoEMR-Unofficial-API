from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Literal


class FieldContent(BaseModel):
    text: Optional[str] = None
    append: bool = True


MaritalStatusOptions = Literal["Single", "Married", "Divorced", "Widowed", "Has Significant Other"]
# Define tobacco use status options
TobaccoStatusOptions = Literal["Non Smoker", "Never Smoked", "Smoker", "Ex-Smoker"]

# Define how often options
TobaccoFrequencyOptions = Literal[
    "Tobacco smoking consumption unknown", "Smokes tobacco daily", "Occasional tobacco smoker"]

# Define intensity options
TobaccoIntensityOptions = Literal["Light tobacco smoker", "Heavy tobacco smoker"]

# Define e-cigarette options
ECigaretteOptions = Literal["Electronic cigarette user"]

# Define tobacco type options
TobaccoTypeOptions = Literal["Pipe smoker", "Snuff User", "Chews tobacco", "Use of moist powdered tobacco"]

# Define smokeless tobacco options
SmokelessTobaccoOptions = Literal["Smokeless tobacco NON user", "User of smokeless tobacco"]

# Define exposure options
TobaccoExposureOptions = Literal[
    "Exposed to tobacco smoke at home", "Exposed to tobacco smoke at work", "No known exposure to tobacco smoke"]

# Define smoking cessation intervention options
SmokingCessationOptions = Literal[
    "Not Discussed", "Advised to Quit", "Discussed Cessation Methods", "Discussed Cessation Medications"]

# Define family cancer history options
FamilyCancerHistoryOptions = Literal["Has Cancer History", "None"]

# Define review of system options - weight
ROSWeightOptions = Literal["No Weight Loss", "Weight Loss"]

# Define review of system options - fatigue
ROSFatigueOptions = Literal["No Fatigue", "Fatigue"]

# Define review of system options - appetite
ROSAppetiteOptions = Literal["No Loss of Appetite", "Loss of Appetite"]

# Define review of system options - night sweats
ROSNightSweatsOptions = Literal["No night sweats", "Night sweats"]

# Define review of system options - fever
ROSFeverOptions = Literal["No fever", "Fever"]

# Define review of system options - chills
ROSChillsOptions = Literal["No Chills", "Chills"]

ROSEyesBlurredVisionOptions = Literal["No Blurred Vision", "Blurred Vision"]
ROSEyesDoubleVisionOptions = Literal["No Double Vision", "Double Vision"]
ROSEyesDifficultyOptions = Literal["No difficulty seeing", "Difficulty Seeing"]

ROSENMTHearingOptions = Literal["No Hearing Loss", "Hearing Loss"]
ROSENMTRingingOptions = Literal["No Ringing in Ears", "Ringing in Ears"]
ROSENMTSinusOptions = Literal["No Sinus Trouble", "Sinus Trouble"]
ROSENMTSwallowingOptions = Literal["No Trouble Swallowing", "Trouble Swallowing"]
ROSENMTThroatOptions = Literal["No Sore Throat", "Sore Throat"]
ROSENMTNasalOptions = Literal["No Nasal drainage", "Nasal drainage"]
ROSENMTNoseBleedOptions = Literal["No Nose Bleeds", "Nose Bleeds"]

# New Literal types for cardiac
ROSCardiacChestPainOptions = Literal["No Chest Pains", "Chest Pains"]
ROSCardiacPalpitationsOptions = Literal["No Heart Palpitations", "Heart Palpitations"]
ROSCardiacLightheadednessOptions = Literal["No Lightheadedness", "Lightheadedness"]
ROSCardiacLegSwellingOptions = Literal["No Swelling in Legs", "Swelling in Legs"]
ROSCardiacSyncopeOptions = Literal["No Syncope", "Syncope"]

# Respiratory system literals
ROSRespCoughOptions = Literal["No Cough", "Cough"]
ROSRespSputumOptions = Literal["No Sputum Production", "Sputum Production"]
ROSRespHemoptysisOptions = Literal["No Hemoptysis", "Hemoptysis"]
ROSRespBreathOptions = Literal["No Shortness of Breath", "Shortness of Breath"]
ROSRespOrthopneaOptions = Literal["No Orthopnea", "Orthopnea"]
ROSRespNPDOptions = Literal["No Nocturnal Paroxysmal Dyspnea", "Nocturnal Paroxysmal Dyspnea"]

# Gastrointestinal system literals
ROSGastroNauseaOptions = Literal["No Nausea", "Nausea"]
ROSGastroVomitingOptions = Literal["No Vomiting", "Vomiting"]
ROSGastroHeartburnOptions = Literal["No Heartburn", "Heartburn"]
ROSGastroConstipationOptions = Literal["No Constipation", "Constipation"]
ROSGastroDiarrheaOptions = Literal["No Diarrhea", "Diarrhea"]
ROSGastroAbdominalPainOptions = Literal["No Abdominal Pain", "Abdominal Pain"]
ROSGastroRectalBleedingOptions = Literal["No Rectal Bleeding", "Rectal Bleeding"]
ROSGastroBowelIncontinenceOptions = Literal["No Bowel Incontinence", "Bowel Incontinence"]

# Genitourinary system literals
ROSGenitoBurningOptions = Literal["No Burning on Urination", "Burning on Urination"]
ROSGenitoPainOptions = Literal["No Pain with Urination", "Pain with Urination"]
ROSGenitoUrgencyOptions = Literal["No Urgency", "Urgency"]
ROSGenitoBloodOptions = Literal["No Blood in Urine", "Blood in Urine"]
ROSGenitoFrequencyOptions = Literal["No Frequent Urination", "Frequent Urination"]
ROSGenitoIncontinenceOptions = Literal["No Urinary Incontinence", "Urinary Incontinence"]

# Skeletal/Musculoskeletal system literals
ROSSkelMusclePainOptions = Literal["No Muscle Pain", "Muscle Pain"]
ROSSkelStiffnessOptions = Literal["No Stiffness", "Stiffness"]
ROSSkelJointPainOptions = Literal["No Joint Pain", "Joint Pain"]
ROSSkelJointSwellingOptions = Literal["No joint swelling", "Joint swelling"]
ROSSkelBackPainOptions = Literal["No Back Pain", "Back Pain"]

ROSSkinRashOptions = Literal["Not Asked", "No skin rash(es)", "Skin Rash", "Other skin complaints"]

# Neurological system literals
ROSNeuroHeadacheOptions = Literal["No Headaches", "Headaches"]
ROSNeuroSeizuresOptions = Literal["No Seizures", "Seizures"]
ROSNeuroDizzinessOptions = Literal["No Dizziness", "Dizziness"]
ROSNeuroBalanceOptions = Literal["No Loss of Balance", "Loss of Balance"]
ROSNeuroWeaknessOptions = Literal["No Weakness of Limbs", "Weakness of Limbs"]
ROSNeuroSensationOptions = Literal["No Loss of Sensation", "Loss of Sensation"]
ROSNeuroTinglingOptions = Literal["No Tingling Sensations", "Tingling Sensations"]
ROSNeuroMemoryOptions = Literal["No Memory Loss", "Memory Loss"]
ROSNeuroThinkingOptions = Literal["No Thinking Difficulty", "Thinking Difficulty"]

# Psychiatric system literals
ROSPsycSystemOptions = Literal["Deferred", "System"]
ROSPsycNervousnessOptions = Literal["No Nervousness", "Nervousness"]
ROSPsycDepressionOptions = Literal["No Depression", "Depression"]
ROSPsycRestlessnessOptions = Literal["No restlessness", "Restless"]
ROSPsycSleepOptions = Literal["No difficulty sleeping", "Difficulty sleeping"]

# Hematologic system literals
ROSHemaBruisingOptions = Literal["No bruising", "Bruising"]
ROSHemaBleedingOptions = Literal["No Bleeding", "Bleeding"]
ROSHemaArmPitsOptions = Literal["No Lumps in Arm Pits", "Lumps in Arm Pits"]
ROSHemaNeckOptions = Literal["No Lumps in Neck", "Lumps in Neck"]
ROSHemaGroinOptions = Literal["No Lumps in Groin", "Lumps in Groin"]

ChaperoneOptions = Literal["Accepted", "Declined"]

# Physical Exam - General literals
PEGeneralNutritionOptions = Literal["Well developed, well nourished", "Malnourished/cachectic"]
PEGeneralDistressOptions = Literal["No acute Distress", "Acutely ill-looking", "Chronicly Ill looking"]
PEGeneralAgeOptions = Literal["Appears Stated age", "Elderly appearance"]

PEHeadTraumaOptions = Literal["Atraumatic and normocephalic", "Traumatic with a wound/scar on the scalp/face"]

# Physical Exam - Eyes literals
PEEyesPupilsOptions = Literal["PERRLA", "Unequal"]
PEEyesEOMOptions = Literal["EOMs intact", "Deviation"]
PEEyesScleraOptions = Literal["No icteric sclera", "Icteric sclera"]
PEEyesConjunctivaOptions = Literal["Conjunctiva Clear", "Conjunctiva red/drainage"]

# Physical Exam - ENMT literals
PEENMTTracheaOptions = Literal["Trachea Midline", "Deviated trachea"]
PEENMTJVDOptions = Literal["NO JVD", "Engorged jugular vessels"]
PEENMTLymphOptions = Literal["No Lymphadenopathy", "Lymphadenopathy"]
PEENMTThyroidOptions = Literal["Thyroid Midline-Normal", "Thyroid enlarged/asymmetric"]
PEENMTOralOptions = Literal["No oral lesions", "Oral abnormality(ies) as noted"]

# Physical Exam - Cardiac literals
PECardiacS12Options = Literal["S1, S2 no mumurs", "S1, S2 mumurs present."]
PECardiacS34Options = Literal["S3,S4 no gallop", "S3/S4 gallop present"]
PECardiacRubsOptions = Literal["No rubs or clicks", "Rub click noted"]
PECardiacBruitsOptions = Literal["No bruits", "Bruits"]
PECardiacRhythmOptions = Literal["Regular heart beat", "Atrial fibrillation"]
PECardiacHeaveOptions = Literal["No parasternal heave", "Parasternal Heave"]
PECardiacRadialOptions = Literal["Radial Pulse Present", "Radial pulses absent"]
PECardiacFemoralOptions = Literal["Femoral Pulses present", "Femoral pulses absent"]
PECardiacPedalOptions = Literal["Pedal Pulses present", "Pedal Pulses absent"]

# Physical Exam - Chest literals
PEChestSymmetryOptions = Literal["Symmetrical", "Asymmetrical"]
PEChestKyphosisOptions = Literal["No kyphosis", "Kyphosis"]
PEChestScoliosisOptions = Literal["No scoliosis", "Scoliosis noted"]

# Physical Exam - Respiratory literals
PERespLungSoundsOptions = Literal["Clear, No rales/Rhonchi", "Rales/Rhonchi present", "Pleural Effusion"]
PERespPercussionOptions = Literal["Percussion and palpation-Normal", "Percussion and palpation abnormal"]

# Physical Exam - Abdomen literals
PEAbdomenConsistencyOptions = Literal["Abdomen soft", "Abdomen firmness"]
PEAbdomenTendernessOptions = Literal["Abdomen non-tender", "Abdomen Tender"]
PEAbdomenDistensionOptions = Literal["Abdomen non-distended", "Abdomen Distended"]
PEAbdomenMassesOptions = Literal["Abdomen without masses", "Abdomen Mass(es)"]
PEAbdomenAscitesOptions = Literal["No Ascites", "Ascites"]
PEAbdomenHepatoOptions = Literal["No hepatomegaly", "Hepatomegaly"]
PEAbdomenSplenoOptions = Literal["No splenomegaly", "Splenomegaly"]
PEAbdomenHerniaOptions = Literal["No hernia", "Hernia"]
PEAbdomenBowelSoundsOptions = Literal["Bowel sounds -Normal", "Bowel sounds -abnormal"]

PEMusculoskeletalStatusOptions = Literal[
    "Deferred"]  # Might need more options if other radio buttons use name="FD_rdoNEG"
PEMusculoskeletalGaitOptions = Literal["Normal gait and station", "Abnormal gait and station"]
PEMusculoskeletalROMOptions = Literal["Range of motion normal", "Decreased range of motion"]
PEMusculoskeletalToneOptions = Literal["Strength/Tone normal", "Strength/Tone decreased"]
PEMusculoskeletalStatureOptions = Literal["Stature Normal", "Loss of Stature"]

# --- NEW Literals for Physical Exam - Extremities ---
PEExtremitiesStatusOptions = Literal["Not examined"]
PEExtremitiesEdemaOptions = Literal["Edema-None", "Edema Present"]
PEExtremitiesCyanosisOptions = Literal["Cyanosis-none", "Cyanosis-Present"]
PEExtremitiesClubbingOptions = Literal["Digital Clubbing-None", "Digital clubbing-present"]
PEExtremitiesDiscolorationOptions = Literal["Discoloration-none", "Discoloration-Present"]

# --- NEW Literals for Physical Exam - Skin ---
PESkinStatusOptions = Literal["System", "Abnormal"]

# --- NEW Literals for Physical Exam - Neurologic ---
PENeurologicAlertnessOptions = Literal["Alert and Oriented", "Altered orientation/alertness"]
PENeurologicSpeechOptions = Literal["Normal Speech", "Abnormal Speech"]
PENeurologicHemiplegiaOptions = Literal["No hemiplegia", "Hemiplegia"]
PENeurologicHemiparesisOptions = Literal["No hemiparesis", "Hemiparesis"]
PENeurologicCranialNervesOptions = Literal["Cranial nerves intact", "Paralysis cranial nerves"]
PENeurologicSensoryOptions = Literal["No sensory deficits", "Sensory deficits"]
PENeurologicMotorOptions = Literal["No motor deficits", "Motor deficits"]

# --- NEW Literals for Physical Exam - Rectal ---
PERectalOccultBloodOptions = Literal["Occult blood negative", "Occult blood positive"]
PERectalMassesOptions = Literal["No masses", "Mass(es)"]

# --- NEW Literals for Physical Exam - GU ---
PEGUProstateOptions = Literal["Prostate Normal", "Prostate Abnormal"]

# --- NEW Literals for Assessment/Plan ---
AssessmentStatusOptions = Literal["NED", "Stable", "Partial Response", "Complete Response", "Progression of Disease"]
ACPLivingWillOptions = Literal["Yes", "No", "Unknown"]
ACPPOAOptions = Literal["Yes", "No", "Unknown"]
ACPPOLSTOptions = Literal["Yes", "No", "Unknown"]
ACPDNROptions = Literal["Yes", "No", "Unknown"]
ACPGoalOfCareOptions = Literal["Palliative", "Curative", "Hospice"]

# --- NEW Literals for Time Spent (Simplified Values) ---
LengthOfVisitOptions = Literal[
    "30 min (99214)",
    "39 min (99214)",
    "40 min (99215)",
    "54 min (99215)",
    "Other"
]

# --- NEW Literals for Social History - Drug Use ---
SHDrugUseStatusOptions = Literal["Negative", "Positive"]

# --- NEW Literals for Social History - Alcohol Use ---
SHAlcoholUseStatusOptions = Literal["Not Asked", "Never", "Currently uses", "Former use"]


class FollowupNoteTemplateModel(BaseModel):
    patient_id: str
    chief_complaint: FieldContent = Field(default_factory=FieldContent)
    disease_history: FieldContent = Field(default_factory=FieldContent)
    interim_history: FieldContent = Field(default_factory=FieldContent)
    past_medical_history: FieldContent = Field(default_factory=FieldContent)
    past_surgical_history: FieldContent = Field(default_factory=FieldContent)
    primary_occupation: FieldContent = Field(default_factory=FieldContent)
    secondary_occupation: FieldContent = Field(default_factory=FieldContent)
    review_of_systems: FieldContent = Field(default_factory=FieldContent)
    physician_note_on_depression_score: FieldContent = Field(default_factory=FieldContent)
    physical_exam: FieldContent = Field(default_factory=FieldContent)
    other_lab_studies: FieldContent = Field(default_factory=FieldContent)
    radiology_results: FieldContent = Field(default_factory=FieldContent)
    assessment: FieldContent = Field(default_factory=FieldContent)
    plan: FieldContent = Field(default_factory=FieldContent)

    # Use Optional[Literal] for radio button fields
    marital_status: Optional[MaritalStatusOptions] = None

    # Tobacco use fields
    tobacco_status: Optional[TobaccoStatusOptions] = None
    tobacco_frequency: Optional[TobaccoFrequencyOptions] = None
    tobacco_intensity: Optional[TobaccoIntensityOptions] = None
    ecigarette_use: Optional[ECigaretteOptions] = None
    tobacco_type: Optional[TobaccoTypeOptions] = None
    smokeless_tobacco: Optional[SmokelessTobaccoOptions] = None
    tobacco_exposure: Optional[TobaccoExposureOptions] = None
    smoking_cessation: Optional[SmokingCessationOptions] = None

    # --- NEW Social History - Tobacco Use History Fields ---
    sh_tobacco_discontinued_year_enabled: Optional[bool] = None # Checkbox: FD_chkSHTobUse_20
    sh_tobacco_pack_years_enabled: Optional[bool] = None        # Checkbox: FD_chkSHTobUse_PH
    sh_tobacco_type_details_enabled: Optional[bool] = None      # Checkbox: FD_chkSHTobUse_KIND

    # Family History fields
    mother_cancer_history: Optional[FamilyCancerHistoryOptions] = None
    father_cancer_history: Optional[FamilyCancerHistoryOptions] = None
    siblings_cancer_history: Optional[FamilyCancerHistoryOptions] = None
    children_cancer_history: Optional[FamilyCancerHistoryOptions] = None
    other_family_history: Optional[bool] = None

    # Review of Systems fields
    ros_system_negative: Optional[bool] = None  # Checkbox
    ros_weight: Optional[ROSWeightOptions] = None
    ros_fatigue: Optional[ROSFatigueOptions] = None
    ros_appetite: Optional[ROSAppetiteOptions] = None
    ros_night_sweats: Optional[ROSNightSweatsOptions] = None
    ros_fever: Optional[ROSFeverOptions] = None
    ros_chills: Optional[ROSChillsOptions] = None

    ros_eyes_negative: Optional[bool] = None  # Checkbox for "System"
    ros_eyes_blurred_vision: Optional[ROSEyesBlurredVisionOptions] = None
    ros_eyes_double_vision: Optional[ROSEyesDoubleVisionOptions] = None
    ros_eyes_difficulty_seeing: Optional[ROSEyesDifficultyOptions] = None

    # ENMT fields
    ros_enmt_negative: Optional[bool] = None
    ros_enmt_hearing: Optional[ROSENMTHearingOptions] = None
    ros_enmt_ringing: Optional[ROSENMTRingingOptions] = None
    ros_enmt_sinus: Optional[ROSENMTSinusOptions] = None
    ros_enmt_swallowing: Optional[ROSENMTSwallowingOptions] = None
    ros_enmt_throat: Optional[ROSENMTThroatOptions] = None
    ros_enmt_nasal: Optional[ROSENMTNasalOptions] = None
    ros_enmt_nasal_details: Optional[str] = None
    ros_enmt_nosebleeds: Optional[ROSENMTNoseBleedOptions] = None
    ros_enmt_hoarseness: Optional[bool] = None

    # Cardiac fields
    ros_cardiac_negative: Optional[bool] = None
    ros_cardiac_chest_pain: Optional[ROSCardiacChestPainOptions] = None
    ros_cardiac_palpitations: Optional[ROSCardiacPalpitationsOptions] = None
    ros_cardiac_lightheadedness: Optional[ROSCardiacLightheadednessOptions] = None
    ros_cardiac_leg_swelling: Optional[ROSCardiacLegSwellingOptions] = None
    ros_cardiac_syncope: Optional[ROSCardiacSyncopeOptions] = None
    ros_cardiac_no_raynauds: Optional[bool] = None
    ros_cardiac_raynauds: Optional[bool] = None

    # Respiratory fields
    ros_resp_negative: Optional[bool] = None
    ros_resp_cough: Optional[ROSRespCoughOptions] = None
    ros_resp_sputum: Optional[ROSRespSputumOptions] = None
    ros_resp_hemoptysis: Optional[ROSRespHemoptysisOptions] = None
    ros_resp_shortness_of_breath: Optional[ROSRespBreathOptions] = None
    ros_resp_orthopnea: Optional[ROSRespOrthopneaOptions] = None
    ros_resp_npd: Optional[ROSRespNPDOptions] = None

    # Gastrointestinal fields
    ros_gastro_negative: Optional[bool] = None
    ros_gastro_nausea: Optional[ROSGastroNauseaOptions] = None
    ros_gastro_vomiting: Optional[ROSGastroVomitingOptions] = None
    ros_gastro_heartburn: Optional[ROSGastroHeartburnOptions] = None
    ros_gastro_constipation: Optional[ROSGastroConstipationOptions] = None
    ros_gastro_diarrhea: Optional[ROSGastroDiarrheaOptions] = None
    ros_gastro_abdominal_pain: Optional[ROSGastroAbdominalPainOptions] = None
    ros_gastro_rectal_bleeding: Optional[ROSGastroRectalBleedingOptions] = None
    ros_gastro_bowel_incontinence: Optional[ROSGastroBowelIncontinenceOptions] = None

    # Genitourinary fields
    ros_genito_negative: Optional[bool] = None
    ros_genito_burning: Optional[ROSGenitoBurningOptions] = None
    ros_genito_pain: Optional[ROSGenitoPainOptions] = None
    ros_genito_urgency: Optional[ROSGenitoUrgencyOptions] = None
    ros_genito_blood: Optional[ROSGenitoBloodOptions] = None
    ros_genito_frequency: Optional[ROSGenitoFrequencyOptions] = None
    ros_genito_incontinence: Optional[ROSGenitoIncontinenceOptions] = None

    # Skeletal/Musculoskeletal fields
    ros_skel_negative: Optional[bool] = None
    ros_skel_muscle_pain: Optional[ROSSkelMusclePainOptions] = None
    ros_skel_stiffness: Optional[ROSSkelStiffnessOptions] = None
    ros_skel_joint_pain: Optional[ROSSkelJointPainOptions] = None
    ros_skel_joint_swelling: Optional[ROSSkelJointSwellingOptions] = None
    ros_skel_back_pain: Optional[ROSSkelBackPainOptions] = None

    # Skin fields
    ros_skin_rash: Optional[ROSSkinRashOptions] = None
    ros_skin_other_details: Optional[str] = None

    # Neurological fields
    ros_neuro_negative: Optional[bool] = None
    ros_neuro_headaches: Optional[ROSNeuroHeadacheOptions] = None
    ros_neuro_seizures: Optional[ROSNeuroSeizuresOptions] = None
    ros_neuro_dizziness: Optional[ROSNeuroDizzinessOptions] = None
    ros_neuro_balance: Optional[ROSNeuroBalanceOptions] = None
    ros_neuro_weakness: Optional[ROSNeuroWeaknessOptions] = None
    ros_neuro_sensation: Optional[ROSNeuroSensationOptions] = None
    ros_neuro_tingling: Optional[ROSNeuroTinglingOptions] = None
    ros_neuro_memory: Optional[ROSNeuroMemoryOptions] = None
    ros_neuro_thinking: Optional[ROSNeuroThinkingOptions] = None

    # Psychiatric fields
    ros_psyc_system: Optional[ROSPsycSystemOptions] = None
    ros_psyc_nervousness: Optional[ROSPsycNervousnessOptions] = None
    ros_psyc_depression: Optional[ROSPsycDepressionOptions] = None
    ros_psyc_restlessness: Optional[ROSPsycRestlessnessOptions] = None
    ros_psyc_sleep: Optional[ROSPsycSleepOptions] = None

    # Hematologic fields
    ros_hema_negative: Optional[bool] = None
    ros_hema_bruising: Optional[ROSHemaBruisingOptions] = None
    ros_hema_bleeding: Optional[ROSHemaBleedingOptions] = None
    ros_hema_bleeding_details: Optional[str] = None
    ros_hema_armpits: Optional[ROSHemaArmPitsOptions] = None
    ros_hema_neck: Optional[ROSHemaNeckOptions] = None
    ros_hema_groin: Optional[ROSHemaGroinOptions] = None

    # Endocrine fields
    ros_endo_system: Optional[bool] = None
    ros_endo_no_polydipsia: Optional[bool] = None
    ros_endo_polydipsia: Optional[bool] = None
    ros_endo_no_polyphagia: Optional[bool] = None
    ros_endo_polyphagia: Optional[bool] = None
    ros_endo_no_polyuria: Optional[bool] = None
    ros_endo_polyuria: Optional[bool] = None

    # Treatment Recommendations fields
    treatment_reassess_next_visit: Optional[bool] = None
    treatment_continue_pain_regimen: Optional[bool] = None
    treatment_narcotic_dose_adjusted: Optional[bool] = None
    treatment_narcotic_prescribed: Optional[bool] = None
    treatment_nonnarcotic_dose_adjusted: Optional[bool] = None
    treatment_nonnarcotic_prescribed: Optional[bool] = None
    treatment_psychological_support: Optional[bool] = None
    treatment_patient_education: Optional[bool] = None
    treatment_refer_pain_management: Optional[bool] = None
    treatment_patient_refused: Optional[bool] = None
    treatment_other_provider_pain: Optional[bool] = None

    # Depression Treatment Recommendations
    depression_no_action_needed: Optional[bool] = None
    depression_referral_placed: Optional[bool] = None
    depression_medication_prescribed: Optional[bool] = None
    depression_declined_medication: Optional[bool] = None
    depression_declined_referral: Optional[bool] = None
    depression_other_provider: Optional[bool] = None
    depression_patient_refused: Optional[bool] = None
    depression_functional_capacity: Optional[bool] = None
    depression_bipolar_excluded: Optional[bool] = None

    # Physical Exam - Chaperone field
    physical_exam_chaperone: Optional[ChaperoneOptions] = None

    # Physical Exam - General fields
    pe_general_negative: Optional[bool] = None
    pe_general_nutrition: Optional[PEGeneralNutritionOptions] = None
    pe_general_distress: Optional[PEGeneralDistressOptions] = None
    pe_general_ecog: Optional[str] = None
    pe_general_age: Optional[PEGeneralAgeOptions] = None

    # Physical Exam - Head fields
    pe_head_negative: Optional[bool] = None
    pe_head_not_assessed: Optional[bool] = None
    pe_head_trauma: Optional[PEHeadTraumaOptions] = None

    # Physical Exam - Eyes fields
    pe_eyes_negative: Optional[bool] = None
    pe_eyes_deferred: Optional[bool] = None
    pe_eyes_pupils: Optional[PEEyesPupilsOptions] = None
    pe_eyes_eom: Optional[PEEyesEOMOptions] = None
    pe_eyes_sclera: Optional[PEEyesScleraOptions] = None
    pe_eyes_conjunctiva: Optional[PEEyesConjunctivaOptions] = None

    # Physical Exam - ENMT fields
    pe_enmt_negative: Optional[bool] = None
    pe_enmt_trachea: Optional[PEENMTTracheaOptions] = None
    pe_enmt_jvd: Optional[PEENMTJVDOptions] = None
    pe_enmt_lymph: Optional[PEENMTLymphOptions] = None
    pe_enmt_lymph_details: Optional[str] = None
    pe_enmt_thyroid: Optional[PEENMTThyroidOptions] = None
    pe_enmt_nodes: Optional[bool] = None
    pe_enmt_oral: Optional[PEENMTOralOptions] = None
    pe_enmt_oral_details: Optional[str] = None
    pe_enmt_tracheostomy: Optional[bool] = None

    # Physical Exam - Cardiac fields
    pe_cardiac_negative: Optional[bool] = None
    pe_cardiac_s12: Optional[PECardiacS12Options] = None
    pe_cardiac_s34: Optional[PECardiacS34Options] = None
    pe_cardiac_rubs: Optional[PECardiacRubsOptions] = None
    pe_cardiac_bruits: Optional[PECardiacBruitsOptions] = None
    pe_cardiac_rhythm: Optional[PECardiacRhythmOptions] = None
    pe_cardiac_heave: Optional[PECardiacHeaveOptions] = None
    pe_cardiac_radial: Optional[PECardiacRadialOptions] = None
    pe_cardiac_femoral: Optional[PECardiacFemoralOptions] = None
    pe_cardiac_pedal: Optional[PECardiacPedalOptions] = None

    # Physical Exam - Chest fields
    pe_chest_negative: Optional[bool] = None
    pe_chest_symmetry: Optional[PEChestSymmetryOptions] = None
    pe_chest_kyphosis: Optional[PEChestKyphosisOptions] = None
    pe_chest_scoliosis: Optional[PEChestScoliosisOptions] = None
    pe_chest_also_noted: Optional[bool] = None
    # pe_chest_also_noted_details: Optional[str] = None

    # Physical Exam - Respiratory fields
    pe_resp_negative: Optional[bool] = None
    pe_resp_lung_sounds: Optional[PERespLungSoundsOptions] = None
    pe_resp_percussion: Optional[PERespPercussionOptions] = None
    pe_resp_also_noted: Optional[bool] = None
    # pe_resp_also_noted_details: Optional[str] = None

    # Physical Exam - Abdomen fields
    pe_abdomen_negative: Optional[bool] = None
    pe_abdomen_scars_present: Optional[bool] = None
    pe_abdomen_consistency: Optional[PEAbdomenConsistencyOptions] = None
    pe_abdomen_tenderness: Optional[PEAbdomenTendernessOptions] = None
    pe_abdomen_distension: Optional[PEAbdomenDistensionOptions] = None
    pe_abdomen_masses: Optional[PEAbdomenMassesOptions] = None
    pe_abdomen_ascites: Optional[PEAbdomenAscitesOptions] = None
    pe_abdomen_hepatomegaly: Optional[PEAbdomenHepatoOptions] = None
    pe_abdomen_splenomegaly: Optional[PEAbdomenSplenoOptions] = None
    pe_abdomen_hernia: Optional[PEAbdomenHerniaOptions] = None
    pe_abdomen_bowel_sounds: Optional[PEAbdomenBowelSoundsOptions] = None
    pe_abdomen_ostomy: Optional[bool] = None

    # --- NEW Physical Exam - Musculoskeletal Fields ---
    pe_musculoskeletal_system_negative: Optional[bool] = None  # Checkbox: FD_chkPESkel_Neg
    pe_musculoskeletal_status: Optional[PEMusculoskeletalStatusOptions] = None
    pe_musculoskeletal_gait: Optional[PEMusculoskeletalGaitOptions] = None  # Radio group: FD_rdoMUSGAIT
    pe_musculoskeletal_rom: Optional[PEMusculoskeletalROMOptions] = None  # Radio group: FD_rdoROM
    pe_musculoskeletal_tone: Optional[PEMusculoskeletalToneOptions] = None  # Radio group: FD_rdoTONE
    pe_musculoskeletal_stature: Optional[PEMusculoskeletalStatureOptions] = None
    pe_musculoskeletal_also_noted_enabled: Optional[bool] = None  # Checkbox: FD_chkAlsonoted_1

    # --- NEW Physical Exam - Extremities Fields ---
    pe_extremities_system_negative: Optional[bool] = None  # Checkbox: FD_chkPEExtremities
    pe_extremities_status: Optional[PEExtremitiesStatusOptions] = None  # Radio: FD_rdoNotexamined
    pe_extremities_edema: Optional[PEExtremitiesEdemaOptions] = None  # Radio group: FD_rdoEEDEMA
    pe_extremities_cyanosis: Optional[PEExtremitiesCyanosisOptions] = None  # Radio group: FD_rdoBLUE
    pe_extremities_clubbing: Optional[PEExtremitiesClubbingOptions] = None  # Radio group: FD_rdoDCLUB
    pe_extremities_discoloration: Optional[PEExtremitiesDiscolorationOptions] = None

    # --- NEW Physical Exam - Skin Field ---
    pe_skin_status: Optional[PESkinStatusOptions] = None

    # --- NEW Physical Exam - Neurologic Fields ---
    pe_neurologic_system_negative: Optional[bool] = None  # Checkbox: FD_chkPENeuro_Neg
    pe_neurologic_alertness: Optional[PENeurologicAlertnessOptions] = None  # Radio group: FD_rdoAOO
    pe_neurologic_speech: Optional[PENeurologicSpeechOptions] = None  # Radio group: FD_rdoSPEECH
    pe_neurologic_hemiplegia: Optional[PENeurologicHemiplegiaOptions] = None  # Radio group: FD_rdoHEMI
    pe_neurologic_hemiparesis: Optional[PENeurologicHemiparesisOptions] = None  # Radio group: FD_rdoPARESIS
    pe_neurologic_cranial_nerves: Optional[PENeurologicCranialNervesOptions] = None  # Radio group: FD_rdoCRANN
    pe_neurologic_sensory: Optional[PENeurologicSensoryOptions] = None  # Radio group: FD_rdoSENSORY
    pe_neurologic_motor: Optional[PENeurologicMotorOptions] = None  # Radio group: FD_rdoMDEFECITS

    # --- NEW Physical Exam - Rectal Fields ---
    pe_rectal_system_negative: Optional[bool] = None  # Checkbox: FD_chkPERectal_negative
    pe_rectal_deferred: Optional[bool] = None  # Checkbox: FD_chkPERectal_Deferred
    pe_rectal_occult_blood: Optional[PERectalOccultBloodOptions] = None  # Radio group: FD_rdoRECTAL
    pe_rectal_masses: Optional[PERectalMassesOptions] = None  # Radio group: FD_rdoRMASS

    # --- NEW Physical Exam - GU Fields ---
    pe_gu_system_negative: Optional[bool] = None # Checkbox: FD_chkPEGU_02
    pe_gu_deferred: Optional[bool] = None        # Checkbox: FD_chkPEGU_Deferred
    pe_gu_prostate: Optional[PEGUProstateOptions] = None

    # --- NEW Physical Exam - Peripheral Smear Fields ---
    # Checkboxes (allowing multiple selections)
    pe_peripheral_smear_normal: Optional[bool] = None # Checkbox: FD_chkNormal PS
    pe_peripheral_smear_micro: Optional[bool] = None  # Checkbox: FD_chkMicro PS
    pe_peripheral_smear_macro: Optional[bool] = None  # Checkbox: FD_chkMacro PS

    # --- NEW Assessment/Plan Fields ---
    assessment_status: Optional[AssessmentStatusOptions] = None
    acp_date_of_discussion_enabled: Optional[bool] = None
    acp_living_will: Optional[ACPLivingWillOptions] = None
    acp_poa: Optional[ACPPOAOptions] = None
    acp_polst: Optional[ACPPOLSTOptions] = None
    acp_dnr: Optional[ACPDNROptions] = None
    acp_goal_of_care: Optional[ACPGoalOfCareOptions] = None

    # --- NEW Time Spent Fields (using simplified Literal) ---
    length_of_patient_visit: Optional[LengthOfVisitOptions] = None

    # --- NEW Social History - Occupational Exposure Fields ---
    sh_occupational_exposure_none: Optional[bool] = None      # Checkbox: FD_chkSHOP_Neg
    sh_occupational_exposure_type_enabled: Optional[bool] = None # Checkbox: FD_chkSHOP_TYPE
    sh_occupational_exposure_solvent: Optional[bool] = None   # Checkbox: FD_chkSolventexposure
    sh_occupational_exposure_asbestos: Optional[bool] = None  # Checkbox: FD_chkAsbestosExp
    sh_occupational_exposure_agent_orange: Optional[bool] = None # Checkbox: FD_chkAgentOrangeexp

    # --- NEW Social History - Drug Use Fields ---
    sh_drug_use_status: Optional[SHDrugUseStatusOptions] = None # Radio group: FD_rdoDRUGS
    sh_drug_use_type_enabled: Optional[bool] = None

    # --- NEW Social History - Alcohol Use Fields ---
    sh_alcohol_use_status: Optional[SHAlcoholUseStatusOptions] = None # Radio group: FD_rdoUSES
    sh_alcohol_drinks_per_day_enabled: Optional[bool] = None   # Checkbox: FD_chkSHAlchUse_4
    sh_alcohol_drinks_per_week_enabled: Optional[bool] = None  # Checkbox: FD_chkSHAlchUse_6
    sh_alcohol_drinks_per_month_enabled: Optional[bool] = None # Checkbox: FD_chkSHAlchUse_8
    sh_alcohol_drinks_per_year_enabled: Optional[bool] = None  # Checkbox: FD_chkSHAlchUse_10
    sh_alcohol_stopped_year_enabled: Optional[bool] = None     # Checkbox: FD_chkSHAlchStop

    # --- NEW Social History - Living Arrangements Fields ---
    sh_living_with_spouse: Optional[bool] = None   # Checkbox: FD_chkWithSpouse
    sh_living_alone: Optional[bool] = None         # Checkbox: FD_chkAlone
    sh_living_with_children: Optional[bool] = None # Checkbox: FD_chkWithChildern
    sh_living_nursing_home: Optional[bool] = None  # Checkbox: FD_chkNrsgHome
    sh_living_other_enabled: Optional[bool] = None # Checkbox: FD_chkOther_2

    # --- NEW Health Maintenance Fields ---
    hm_colonoscopy_enabled: Optional[bool] = None # Checkbox: FD_chkPHHS_Colon
    hm_dexascan_enabled: Optional[bool] = None
