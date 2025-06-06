#!/usr/bin/python
# -*- coding: utf-8 -*-
# consultation_mappings.py

# --- Text Field Mappings ---
# Maps ConsultationNoteTemplateModel fields (using FieldContent) to target dictionary keys

CONSULTATION_TEXTFIELDS_MAPPING = {
    "reason_for_consult": "FD_txtDHVT_Reasonforconsult",
    "disease_history": "FD_txtTreatment History",
    "interim_history": "FD_txtHPIT",
    "past_medical_history": "FD_txtPastMedicalHistory",
    "past_surgical_history": "FD_txtPFSHSurgical",
    "hm_colonoscopy_details": "FD_itbPHHS_Colon",
    "hm_dexascan_details": "FD_itbPHHS_Dexascan",
    "sh_living_arrangements_other_details": "FD_itbOther_2",
    "sh_tobacco_discontinued_year": "FD_itbSHTobUse_20",
    "sh_tobacco_pack_years": "FD_itbSHTobUse_PH",
    "sh_tobacco_type_details": "FD_itbSHTobUse_KIND",
    "sh_alcohol_drinks_per_day": "FD_itbSHAlchUse_4",
    "sh_alcohol_drinks_per_week": "FD_itbSHAlchUse_6",
    "sh_alcohol_drinks_per_month": "FD_itbSHAlchUse_8",
    "sh_alcohol_drinks_per_year": "FD_itbSHAlchUse_10",
    "sh_alcohol_stopped_year": "FD_itbSHAlchStop",
    "sh_drug_use_type_details": "FD_itbSHDrugs",
    "primary_occupation": "FD_txtPFSHPrimOcc",
    "secondary_occupation": "FD_txtPFSHSecOcc",
    "sh_occupational_exposure_type_details": "FD_itbSHOP_TYPE",
    "family_history_comment": "FD_txtFHFamHx",
    "mother_cancer_history_details": "FD_itbFHFamCancerMother_Yes",
    "father_cancer_history_details": "FD_itbFHFamCancerFather_Yes",
    "siblings_cancer_history_details": "FD_itbFHFamCancerSiblings_Yes",
    "children_cancer_history_details": "FD_itbFHFamCancerChildren_Yes",
    "other_family_history_details": "FD_itbFHOtherFamHx",
    "review_of_systems": "FD_txtallnormalROS",
    "ros_weight_loss_details": "FD_itbROSCon_4",
    "ros_nasal_drainage_details": "FD_itbNasaldrainage",
    "ros_skin_other_details": "FD_itbOtherskincomplaints",
    "ros_heme_bleeding_details": "FD_itbBleeding_1",
    "physician_note_on_depression_score": "FD_txtPhysicianNoteonDepressionScore",
    "physical_exam": "FD_txtallnormal2",
    "pe_lymphadenopathy_details": "FD_itbPEENMT_12",
    "pe_oral_abnormality_details": "FD_itbOralabnormalityiesasnoted",
    "pe_respiratory_also_noted_details": "FD_itbPEresp_other",
    "pe_abdomen_scars_details": "FD_itbScarspresent",
    "pe_msk_also_noted_details": "FD_itbAlsonoted_1",
    "pe_edema_details": "FD_itbEdemapresent",
    "pe_abnormal_speech_details": "FD_itbAbnormalSpeech",
    "peripheral_smear_comment": "FD_txtPeripheralSmear",
    "other_lab_studies": "FD_txtOLS",
    "radiology_results": "FD_txtRadiologyResults",
    "assessment": "FD_txtDiagnosis",
    "acp_date_of_discussion_details": "FD_itbDOD_ACP",
    "plan": "FD_txtIP_Plan",
    "length_of_patient_visit_other_minutes": "FD_itbOther_1",
}

# Ignored: Grid text fields, summary fields, comment fields tied to radio/checkbox display

# --- Radio Button Mappings ---
# Maps ConsultationNoteTemplateModel fields (using Literal) to target dictionary keys.
# NOTE: Grade Scales (FD_gs...) are excluded as they require special value handling.

CONSULTATION_RADIO_BUTTONS_MAPPING = {  # Using same ID as conj color
    # "pe_msk_status": { "options": {"Deferred": "FD_rdoPESkel_Deferred"} }, # Handled by boolean pe_msk_deferred
    "marital_status": {
        "options": {
            "Single": "FD_rdoSingle",
            "Married": "FD_rdoMarried",
            "Divorced": "FD_rdoDivorced",
            "Widowed": "FD_rdoWidowed",
            "Has Significant Other": "FD_rdoHasSignificantOther",
        }
    },
    "tobacco_status": {
        "options": {
            "1 Current Everyday Smoker": "FD_rdoARRACurrentEverydaySmoker",
            "2 Current Some Day Smoker": "FD_rdoARRACurrentSomeDaySmoker",
            "3 Former Smoker": "FD_rdoARRAFormerSmoker",
            "4 Never Smoker": "FD_rdoARRANeverSmoker",
            "5 Smoker, Current Status Unknown": "FD_rdoARRASmokerStatusUnknown",
            "9 Unknown If Ever Smoked": "FD_rdoARRAUnknownIfEverSmoked",
        }
    },
    "smoking_cessation": {
        "options": {
            "Not Discussed": "FD_rdoARRASCINotDiscussed",
            "Advised to Quit": "FD_rdoARRASCIAdvisedToQuit",
            "Discussed Cessation Methods": "FD_rdoARRASCIDiscussedCessationMethods",
            "Discussed Cessation Medications": "FD_rdoARRASCIDiscussedCessationMedications",
        }
    },
    "sh_alcohol_use_status": {
        "options": {
            "Not Asked": "FD_rdoSHAlchUse_NE",
            "Never": "FD_rdoSHAlchUse_Neg",
            "Currently uses": "FD_rdoCurrentlyuses",
            "Former use": "FD_rdoFormeruse",
        }
    },
    "sh_drug_use_status": {
        "options": {"Negative": "FD_rdoSHDrugs_Neg", "Positive": "FD_rdoSHDrugs_Pos"}
    },
    "mother_cancer_history": {
        "options": {
            "Yes": "FD_rdoFHFamCancerMother_Yes",
            "None": "FD_rdoFHFamCancerMother_No",
        }
    },
    "father_cancer_history": {
        "options": {
            "Yes": "FD_rdoFHFamCancerFather_Yes",
            "None": "FD_rdoFHFamCancerFather_No",
        }
    },
    "siblings_cancer_history": {
        "options": {
            "Yes": "FD_rdoFHFamCancerSiblings_Yes",
            "None": "FD_rdoFHFamCancerSiblings_No",
        }
    },
    "children_cancer_history": {
        "options": {
            "Yes": "FD_rdoFHFamCancerChildren_Yes",
            "None": "FD_rdoFHFamCancerChildren_No",
        }
    },
    "other_family_history_status": {
        "options": {"Other Family History": "FD_rdoFHOtherFamHx"}
    },
    "ros_weight": {
        "options": {
            "No Weight Loss": "FD_rdoROSCon_NWL",
            "Weight Loss": "FD_rdoROSCon_4",
        }
    },
    "ros_fatigue": {
        "options": {"No Fatigue": "FD_rdoROSCon_NF", "Fatigue": "FD_rdoROSCon_F"}
    },
    "ros_appetite": {
        "options": {
            "No Loss of Appetite": "FD_rdoROSCon_NLA",
            "Loss of Appetite": "FD_rdoROSCon_LOA",
        }
    },
    "ros_night_sweats": {
        "options": {
            "No night sweats": "FD_rdoROSCon_02",
            "Night sweats": "FD_rdoROSCon_06",
        }
    },
    "ros_fever": {"options": {"No fever": "FD_rdoNofever", "Fever": "FD_rdoFever"}},
    "ros_chills": {
        "options": {"No Chills": "FD_rdoNoChills", "Chills": "FD_rdoChills"}
    },
    "ros_eyes_blurred_vision": {
        "options": {
            "No Blurred Vision": "FD_rdoROSEyes_NBV",
            "Blurred Vision": "FD_rdoROSEyes_BV",
        }
    },
    "ros_eyes_double_vision": {
        "options": {
            "No Double Vision": "FD_rdoROSEyes_NDV",
            "Double Vision": "FD_rdoROSEyes_DV",
        }
    },
    "ros_eyes_difficulty_seeing": {
        "options": {
            "No difficulty seeing": "FD_rdoNodifficultyseeing",
            "Difficulty Seeing": "FD_rdoDifficultySeeing",
        }
    },
    "ros_enmt_hearing_loss": {
        "options": {
            "No Hearing Loss": "FD_rdoROSENMT_NHL",
            "Hearing Loss": "FD_rdoROSENMT_HL",
        }
    },
    "ros_enmt_ringing_ears": {
        "options": {
            "No Ringing in Ears": "FD_rdoROSENMT_NRIE",
            "Ringing in Ears": "FD_rdoROSENMT_RIE",
        }
    },
    "ros_enmt_sinus_trouble": {
        "options": {
            "No Sinus Trouble": "FD_rdoROSENMT_NST",
            "Sinus Trouble": "FD_rdoROSENMT_ST",
        }
    },
    "ros_enmt_trouble_swallowing": {
        "options": {
            "No Trouble Swallowing": "FD_rdoROSENMT_NTS",
            "Trouble Swallowing": "FD_rdoROSENMT_TS",
        }
    },
    "ros_enmt_sore_throat": {
        "options": {
            "No Sore Throat": "FD_rdoROSENMT_NSOT",
            "Sore Throat": "FD_rdoROSENMT_SOT",
        }
    },
    "ros_enmt_nasal_drainage": {
        "options": {
            "No Nasal drainage": "FD_rdoNoNasaldrainage",
            "Nasal drainage": "FD_rdoNasaldrainage",
        }
    },
    "ros_enmt_nose_bleeds": {
        "options": {
            "No Nose Bleeds": "FD_rdoROSENMT_NNB",
            "Nose Bleeds": "FD_rdoROSENMT_NB",
        }
    },
    "ros_enmt_hoarseness": {"options": {"Hoarseness": "FD_rdoROSENMT_H"}},
    "ros_cardiac_chest_pain": {
        "options": {
            "No Chest Pains": "FD_rdoROSCardiac_NCP",
            "Chest Pains": "FD_rdoROSCardiac_CP",
        }
    },
    "ros_cardiac_palpitations": {
        "options": {
            "No Heart Palpitations": "FD_rdoROSCardiac_NHP",
            "Heart Palpitations": "FD_rdoROSCardiac_HP",
        }
    },
    "ros_cardiac_lightheadedness": {
        "options": {
            "No Lightheadedness": "FD_rdoROSCardiac_NLH",
            "Lightheadedness": "FD_rdoROSCardiac_LH",
        }
    },
    "ros_cardiac_swelling_legs": {
        "options": {
            "No Swelling in Legs": "FD_rdoROSCardiac_NSIL",
            "Swelling in Legs": "FD_rdoROSCardiac_SIL",
        }
    },
    "ros_cardiac_syncope": {
        "options": {
            "No Syncope": "FD_rdoROSCardiac_NEPO",
            "Syncope": "FD_rdoROSCardiac_EPO",
        }
    },
    "ros_resp_cough": {
        "options": {"No Cough": "FD_rdoROSResp_NC", "Cough": "FD_rdoROSResp_C"}
    },
    "ros_resp_sputum": {
        "options": {
            "No Sputum Production": "FD_rdoROSResp_NSP",
            "Sputum Production": "FD_rdoROSResp_SP",
        }
    },
    "ros_resp_hemoptysis": {
        "options": {
            "No Hemoptysis": "FD_rdoROSResp_NH",
            "Hemoptysis": "FD_rdoROSResp_H",
        }
    },
    "ros_resp_sob": {
        "options": {
            "No Shortness of Breath": "FD_rdoROSResp_NSOB",
            "Shortness of Breath": "FD_rdoROSResp_SOB",
        }
    },
    "ros_resp_orthopnea": {
        "options": {"No Orthopnea": "FD_rdoROSResp_NO", "Orthopnea": "FD_rdoROSResp_O"}
    },
    "ros_resp_npd": {
        "options": {
            "No Nocturnal Paroxysmal Dyspnea": "FD_rdoROSResp_NNPD",
            "Nocturnal Paroxysmal Dyspnea": "FD_rdoROSResp_NPD",
        }
    },
    "ros_gi_nausea": {
        "options": {"No Nausea": "FD_rdoROSGastro_NN", "Nausea": "FD_rdoROSGastro_N"}
    },
    "ros_gi_vomiting": {
        "options": {
            "No Vomiting": "FD_rdoROSGastro_NV",
            "Vomiting": "FD_rdoROSGastro_V",
        }
    },
    "ros_gi_heartburn": {
        "options": {
            "No Heartburn": "FD_rdoROSGastro_NHB",
            "Heartburn": "FD_rdoROSGastro_HB",
        }
    },
    "ros_gi_constipation": {
        "options": {
            "No Constipation": "FD_rdoROSGastro_NC",
            "Constipation": "FD_rdoROSGastro_C",
        }
    },
    "ros_gi_diarrhea": {
        "options": {
            "No Diarrhea": "FD_rdoROSGastro_ND",
            "Diarrhea": "FD_rdoROSGastro_D",
        }
    },
    "ros_gi_abdominal_pain": {
        "options": {
            "No Abdominal Pain": "FD_rdoROSGastro_NAP",
            "Abdominal Pain": "FD_rdoROSGastro_AP",
        }
    },
    "ros_gi_rectal_bleeding": {
        "options": {
            "No Rectal Bleeding": "FD_rdoROSGastro_NRB",
            "Rectal Bleeding": "FD_rdoROSGastro_RB",
        }
    },
    "ros_gi_bowel_incontinence": {
        "options": {
            "No Bowel Incontinence": "FD_rdoROSGastro_NBI",
            "Bowel Incontinence": "FD_rdoROSGastro_BI",
        }
    },
    "ros_gu_burning_urination": {
        "options": {
            "No Burning on Urination": "FD_rdoROSGenito_NBU",
            "Burning on Urination": "FD_rdoROSGenito_BU",
        }
    },
    "ros_gu_pain_urination": {
        "options": {
            "No Pain with Urination": "FD_rdoROSGenito_NPU",
            "Pain with Urination": "FD_rdoROSGenito_PU",
        }
    },
    "ros_gu_urgency": {
        "options": {"No Urgency": "FD_rdoROSGU_NU", "Urgency": "FD_rdoROSGU_U"}
    },
    "ros_gu_blood_urine": {
        "options": {
            "No Blood in Urine": "FD_rdoROSGenito_NBIU",
            "Blood in Urine": "FD_rdoROSGenito_BIU",
        }
    },
    "ros_gu_frequent_urination": {
        "options": {
            "No Frequent Urination": "FD_rdoROSGenito_NFU",
            "Frequent Urination": "FD_rdoROSGenito_FU",
        }
    },
    "ros_gu_urinary_incontinence": {
        "options": {
            "No Urinary Incontinence": "FD_rdoROSGenito_NUI",
            "Urinary Incontinence": "FD_rdoROSGenito_UI",
        }
    },
    "ros_msk_muscle_pain": {
        "options": {
            "No Muscle Pain": "FD_rdoROSSkel_NMP",
            "Muscle Pain": "FD_rdoROSSkel_MP",
        }
    },
    "ros_msk_stiffness": {
        "options": {
            "No Stiffness": "FD_rdoROSSkel_NST",
            "Stiffness": "FD_rdoROSSkel_ST",
        }
    },
    "ros_msk_joint_pain": {
        "options": {
            "No Joint Pain": "FD_rdoROSSkel_NJP",
            "Joint Pain": "FD_rdoROSSkel_JP",
        }
    },
    "ros_msk_joint_swelling": {
        "options": {
            "No joint swelling": "FD_rdoNojointswelling",
            "Joint swelling": "FD_rdoJointswelling",
        }
    },
    "ros_msk_back_pain": {
        "options": {
            "No Back Pain": "FD_rdoROSSkel_NBP",
            "Back Pain": "FD_rdoROSSkel_BP",
        }
    },
    "ros_skin_status": {
        "options": {
            "Not Asked": "FD_rdoROSSkin_NE",
            "No skin rash(es)": "FD_rdoROSSkin_Neg",
            "Skin Rash": "FD_rdoROSSkin_SR",
            "Other skin complaints": "FD_rdoOtherskincomplaints",
        }
    },
    "ros_neuro_headaches": {
        "options": {
            "No Headaches": "FD_rdoROSNeuro_NH",
            "Headaches": "FD_rdoROSNeuro_H",
        }
    },
    "ros_neuro_seizures": {
        "options": {"No Seizures": "FD_rdoROSNeuro_NS", "Seizures": "FD_rdoROSNeuro_S"}
    },
    "ros_neuro_dizziness": {
        "options": {
            "No Dizziness": "FD_rdoROSNeuro_ND",
            "Dizziness": "FD_rdoROSNeuro_D",
        }
    },
    "ros_neuro_loss_of_balance": {
        "options": {
            "No Loss of Balance": "FD_rdoROSNeuro_NLOB",
            "Loss of Balance": "FD_rdoROSNeuro_LOB",
        }
    },
    "ros_neuro_weakness_limbs": {
        "options": {
            "No Weakness of Limbs": "FD_rdoROSNeuro_NWOL",
            "Weakness of Limbs": "FD_rdoROSNeuro_WOL",
        }
    },
    "ros_neuro_loss_of_sensation": {
        "options": {
            "No Loss of Sensation": "FD_rdoROSNeuro_NLOS",
            "Loss of Sensation": "FD_rdoROSNeuro_LOS",
        }
    },
    "ros_neuro_tingling": {
        "options": {
            "No Tingling Sensations": "FD_rdoROSNeuro_NTS",
            "Tingling Sensations": "FD_rdoROSNeuro_TS",
        }
    },
    "ros_neuro_memory_loss": {
        "options": {
            "No Memory Loss": "FD_rdoROSNeuro_NML",
            "Memory Loss": "FD_rdoROSNeuro_ML",
        }
    },
    "ros_neuro_thinking_difficulty": {
        "options": {
            "No Thinking Difficulty": "FD_rdoROSNeuro_NTD",
            "Thinking Difficulty": "FD_rdoROSNeuro_TD",
        }
    },
    "ros_psych_status": {
        "options": {"Deferred": "FD_rdoROSPsyc_defer", "System": "FD_rdoROSPsyc_Neg"}
    },
    "ros_psych_nervousness": {
        "options": {
            "No Nervousness": "FD_rdoROSPsyc_NNER",
            "Nervousness": "FD_rdoROSPsyc_NER",
        }
    },
    "ros_psych_depression": {
        "options": {
            "No Depression": "FD_rdoROSPsyc_NDEP",
            "Depression": "FD_rdoROSPsyc_DEP",
        }
    },
    "ros_psych_restlessness": {
        "options": {
            "No restlessness": "FD_rdoNorestlessness",
            "Restless": "FD_rdoRestless",
        }
    },
    "ros_psych_difficulty_sleeping": {
        "options": {
            "No difficulty sleeping": "FD_rdoNodifficultysleeping",
            "Difficulty sleeping": "FD_rdoDifficultysleeping",
        }
    },
    "ros_heme_bruising": {
        "options": {"No bruising": "FD_rdoNObruising", "Bruising": "FD_rdoBruising"}
    },
    "ros_heme_bleeding": {
        "options": {"No Bleeding": "FD_rdoNoBleeding_1", "Bleeding": "FD_rdoBleeding_1"}
    },
    "ros_heme_lumps_armpits": {
        "options": {
            "No Lumps in Arm Pits": "FD_rdoROSHema_NAL",
            "Lumps in Arm Pits": "FD_rdoROSHema_AL",
        }
    },
    "ros_heme_lumps_neck": {
        "options": {
            "No Lumps in Neck": "FD_rdoROSHema_NN",
            "Lumps in Neck": "FD_rdoROSHema_N",
        }
    },
    "ros_heme_lumps_groin": {
        "options": {
            "No Lumps in Groin": "FD_rdoROSHema_NG",
            "Lumps in Groin": "FD_rdoROSHema_G",
        }
    },
    "pe_chaperone_status": {
        "options": {
            "Accepted": "FD_rdoChaperone_Accepted",
            "Declined": "FD_rdoChaperone_Declined",
        }
    },
    "pe_general_nutrition": {
        "options": {
            "Well developed, well nourished": "FD_rdoPEGeneral_02",
            "Malnourished/cachectic": "FD_rdoPEGeneral_04",
        }
    },
    "pe_general_distress": {
        "options": {
            "No acute Distress": "FD_rdoPEGeneral_06",
            "Acutely ill-looking": "FD_rdoPEGeneral_08",
            "Chronicly Ill looking": "FD_rdoChroniclyIlllooking",
        }
    },
    "pe_general_age_appearance": {
        "options": {
            "Appears Stated age": "FD_rdoPEGeneral_14",
            "Elderly appearance": "FD_rdoPEGeneral_16",
        }
    },
    "pe_head_trauma": {
        "options": {
            "Atraumatic and normocephalic": "FD_rdoAtraumaticandnormocephalic",
            "Traumatic with a wound/scar on the scalp/face.": "FD_rdoTraumaticwithawoundscaronthescalpface",
        }
    },
    "pe_eyes_perrla": {
        "options": {"PERRLA": "FD_rdoPEEyes_02", "Unequal": "FD_rdoPEEyes_04"}
    },
    "pe_eyes_conjunctiva_color": {
        "options": {
            "Pink palpebral conjunctivae": "FD_rdoPEEyes_06",
            "Slightly pale palpebral conjunctivae": "FD_rdoPEEyes_08",
        }
    },
    "pe_eyes_eom": {
        "options": {"EOMs intact": "FD_rdoPEEyes_10", "Deviation": "FD_rdoPEEyes_12"}
    },
    "pe_eyes_sclera": {
        "options": {
            "No icteric sclera": "FD_rdoPEEyes_06",
            "Icteric sclera": "FD_rdoPEEyes_08",
        }
    },
    "pe_eyes_conjunctiva_clarity": {
        "options": {
            "Conjunctiva Clear": "FD_rdoPEEyes_14",
            "Conjunctiva red/drainage": "FD_rdoPEEyes_16",
        }
    },
    "pe_enmt_trachea": {
        "options": {
            "Trachea Midline": "FD_rdoPEENMT_02",
            "Deviated trachea": "FD_rdoPEENMT_04",
        }
    },
    "pe_enmt_jvd": {
        "options": {
            "NO JVD": "FD_rdoPEENMT_06",
            "Engorged jugular vessels": "FD_rdoPEENMT_08",
        }
    },
    "pe_enmt_lymphadenopathy": {
        "options": {
            "No Lymphadenopathy": "FD_rdoPEENMT_10",
            "Lymphadenopathy": "FD_rdoPEENMT_12",
        }
    },
    "pe_enmt_thyroid": {
        "options": {
            "Thyroid Midline-Normal": "FD_rdoPEENMT_14",
            "Thyroid enlarged/asymmetric": "FD_rdoPEENMT_16",
        }
    },
    "pe_enmt_oral_lesions": {
        "options": {
            "No oral lesions": "FD_rdoNoorallesions",
            "Oral abnormality(ies) as noted": "FD_rdoOralabnormalityiesasnoted",
        }
    },
    "pe_cardiac_s1s2": {
        "options": {
            "S1, S2 no mumurs": "FD_rdoPECardiac_02",
            "S1, S2 mumurs present.": "FD_rdoPECardiac_04",
        }
    },
    "pe_cardiac_s3s4": {
        "options": {
            "S3,S4 no gallop": "FD_rdoPECardiac_06",
            "S3/S4 gallop present": "FD_rdoPECardiac_08",
        }
    },
    "pe_cardiac_rubs_clicks": {
        "options": {
            "No rubs or clicks": "FD_rdoNorubsorclicks",
            "Rub click noted": "FD_rdoRubclicknoted",
        }
    },
    "pe_cardiac_bruits": {
        "options": {"No bruits": "FD_rdoPECardiac_10", "Bruits": "FD_rdoPECardiac_12"}
    },
    "pe_cardiac_rhythm": {
        "options": {
            "Regular heart beat": "FD_rdoPECardiac_14",
            "Atrial fibrillation": "FD_rdoPECardiac_16",
        }
    },
    "pe_cardiac_heave": {
        "options": {
            "No parasternal heave": "FD_rdoPECardiac_18",
            "Parasternal Heave": "FD_rdoPECardiac_20",
        }
    },
    "pe_cardiac_radial_pulse": {
        "options": {
            "Radial Pulse Present": "FD_rdoRadialPulsePresent",
            "Radial pulses absent": "FD_rdoRadialpulsesabsent",
        }
    },
    "pe_cardiac_femoral_pulse": {
        "options": {
            "Femoral Pulses present": "FD_rdoPECardiac_22",
            "Femoral pulses absent": "FD_rdoPECardiac_24",
        }
    },
    "pe_cardiac_pedal_pulse": {
        "options": {
            "Pedal Pulses present": "FD_rdoPedalPulsespresent",
            "Pedal Pulses absent": "FD_rdoPedalPulsesabsent",
        }
    },
    "pe_resp_auscultation": {
        "options": {
            "Clear, No rales/Rhonchi": "FD_rdoPEResp_02",
            "Rales/Rhonchi present": "FD_rdoPEResp_04",
            "Pleural Effusion": "FD_rdoPEResp_06",
        }
    },
    "pe_resp_percussion_palpation": {
        "options": {
            "Percussion and palpation-Normal": "FD_rdoPercussionandpalpation",
            "Percussion and palpation abnormal": "FD_rdoPercussionandpalpationabnormal",
        }
    },
    "pe_gi_firmness": {
        "options": {
            "Abdomen soft": "FD_rdoPEAbdomen_20",
            "Abdomen firmness": "FD_rdoPEAbdomen_21",
        }
    },
    "pe_gi_tenderness": {
        "options": {
            "Abdomen non-tender": "FD_rdoPEAbdomen_22",
            "Abdomen Tender": "FD_rdoPEAbdomen_25",
        }
    },
    "pe_gi_distension": {
        "options": {
            "Abdomen non-distended": "FD_rdoPEAbdomen_23",
            "Abdomen Distended": "FD_rdoPEAbdomen_27",
        }
    },
    "pe_gi_masses": {
        "options": {
            "Abdomen without masses": "FD_rdoPEAbdomen_24",
            "Abdomen Mass(es)": "FD_rdoPEAbdomen_29",
        }
    },
    "pe_gi_ascites": {
        "options": {"No Ascites": "FD_rdoPEAbdomen_32", "Ascites": "FD_rdoPEAbdomen_26"}
    },
    "pe_gi_hepatomegaly": {
        "options": {
            "No hepatomegaly": "FD_rdoPEAbdomen_NoHepato",
            "Hepatomegaly": "FD_rdoPEAbdomen_Hepato",
        }
    },
    "pe_gi_splenomegaly": {
        "options": {
            "No splenomegaly": "FD_rdoPEAbdomen_NoSpleno",
            "Splenomegaly": "FD_rdoPEAbdomen_Spleno",
        }
    },
    "pe_gi_hernia": {
        "options": {"No hernia": "FD_rdoNohernia", "Hernia": "FD_rdoHernia"}
    },
    "pe_gi_bowel_sounds": {
        "options": {
            "Bowel sounds -Normal": "FD_rdoBowelsounds-Normal",
            "Bowel sounds -abnormal": "FD_rdoBowelsounds-abnormal",
        }
    },
    "pe_msk_gait": {
        "options": {
            "Normal gait and station": "FD_rdoPESkel_23",
            "Abnormal gait and station": "FD_rdoPESkel_24",
        }
    },
    "pe_msk_rom": {
        "options": {
            "Range of motion normal": "FD_rdoPESkel_26",
            "Decreased range of motion": "FD_rdoPESkel_28",
        }
    },
    "pe_msk_tone": {
        "options": {
            "Strength/Tone normal": "FD_rdoPESkel_30",
            "Strength/Tone decreased": "FD_rdoPESkel_32",
        }
    },
    "pe_msk_stature": {
        "options": {
            "Stature Normal": "FD_rdoPESkel_34",
            "Loss of Stature": "FD_rdoPESkel_36",
        }
    },
    "pe_extremities_status": {"options": {"Not examined": "FD_rdoNotexamined"}},
    "pe_extremities_edema": {
        "options": {
            "Edema-None": "FD_rdoEdema-None",
            "Edema Present": "FD_rdoEdemapresent",
        }
    },
    "pe_extremities_cyanosis": {
        "options": {
            "Cyanosis-none": "FD_rdoCyanosis-none",
            "Cyanosis-Present": "FD_rdoCyanosis-Present",
        }
    },
    "pe_extremities_clubbing": {
        "options": {
            "Digital Clubbing-None": "FD_rdoDigitalClubbing-None",
            "Digital clubbing-present": "FD_rdoDigitalclubbing-present",
        }
    },
    "pe_extremities_discoloration": {
        "options": {
            "Discoloration-none": "FD_rdoDiscoloration-none",
            "Discoloration-Present": "FD_rdoDiscoloration-Present",
        }
    },
    "pe_skin_status": {
        "options": {"System": "FD_rdoPESkin_Neg", "Abnormal": "FD_rdoPESkin_ABN"}
    },
    "pe_neuro_alertness": {
        "options": {
            "Alert and Oriented": "FD_rdoAlertandOriented",
            "Altered orientation/alertness": "FD_rdoAlertedorientationalertness",
        }
    },
    "pe_neuro_speech": {
        "options": {
            "Normal Speech": "FD_rdoNormalSpeech",
            "Abnormal Speech": "FD_rdoAbnormalSpeech",
        }
    },
    "pe_neuro_hemiplegia": {
        "options": {
            "No hemiplegia": "FD_rdoPENeurologic_24",
            "Hemiplegia": "FD_rdoPENeurologic_26",
        }
    },
    "pe_neuro_hemiparesis": {
        "options": {
            "No hemiparesis": "FD_rdoNohemiparesis",
            "Hemiparesis": "FD_rdoHemiparesis",
        }
    },
    "pe_neuro_cranial_nerves": {
        "options": {
            "Cranial nerves intact": "FD_rdoPENeurologic_28",
            "Paralysis cranial nerves": "FD_rdoPENeurologic_30",
        }
    },
    "pe_neuro_sensory": {
        "options": {
            "No sensory deficits": "FD_rdoPENeurologic_32",
            "Sensory deficits": "FD_rdoPENeurologic_34",
        }
    },
    "pe_neuro_motor": {
        "options": {
            "No motor deficits": "FD_rdoPENeurologic_36",
            "Motor deficits": "FD_rdoPENeurologic_38",
        }
    },
    "pe_rectal_occult_blood": {
        "options": {
            "Occult blood negative": "FD_rdoPERectal_02",
            "Occult blood positive": "FD_rdoPERectal_04",
        }
    },
    "pe_rectal_masses": {
        "options": {"No masses": "FD_rdoPERectal_06", "Mass(es)": "FD_rdoPERectal_08"}
    },
    "pe_gu_prostate": {
        "options": {
            "Prostate Normal": "FD_rdoPEGU_PN",
            "Prostate Abnormal": "FD_rdoPEGU_04",
        }
    },
    "assessment_status": {
        "options": {
            "NED": "FD_rdoMDMassess_01",
            "Stable": "FD_rdoMDMassess_02",
            "Partial Response": "FD_rdoMDMassess_04",
            "Complete Response": "FD_rdoMDMassess_06",
            "Progression of Disease": "FD_rdoMDMassess_08",
        }
    },
    "acp_living_will": {
        "options": {
            "Yes": "FD_rdoYes_LivingWill",
            "No": "FD_rdoNo_LivingWill",
            "Unknown": "FD_rdoUnknown_LivingWill",
        }
    },
    "acp_poa": {
        "options": {
            "Yes": "FD_rdoYes_POA",
            "No": "FD_rdoNo_POA",
            "Unknown": "FD_rdoUnknown_POA",
        }
    },
    "acp_polst": {
        "options": {
            "Yes": "FD_rdoYes_POLST",
            "No": "FD_rdoNo_POLST",
            "Unknown": "FD_rdoUnknown_POLST",
        }
    },
    "acp_dnr": {
        "options": {
            "Yes": "FD_rdoYes_DNR",
            "No": "FD_rdoNo_DNR",
            "Unknown": "FD_rdoUnknown_DNR",
        }
    },
    "acp_goal_of_care": {
        "options": {
            "Palliative": "FD_rdoPalliative_ACP",
            "Curative": "FD_rdoCurative_ACP",
            "Hospice": "FD_rdoHospice_ACP",
        }
    },
    "length_of_patient_visit": {
        "options": {
            "Visit length 30 minutes (99203)": "FD_rdoLenPtVisit_10",
            "Visit length 44 minutes (99203)": "FD_rdoLenPtVisit_12",
            "Visit length 45 minutes (99204)": "FD_rdoLenPtVisit_04",
            "Visit length 59 minutes (99204)": "FD_rdoLenPtVisit_09",
            "Visit length 60 minutes (99205)": "FD_rdoLenPtVisit_03",
            "Visit length 74 minutes (99205)": "FD_rdoLenPtVisit_08",
            "Other": "FD_rdoOther_1",
        }
    },
    "mdm_level": {
        "options": {
            "High": "FD_rdoHigh",
            "Moderate": "FD_rdoModerate",
            "Low": "FD_rdoLow",
            "Straightforward": "FD_rdoStraightforward",
        }
    },
}

# --- Checkbox Mappings ---
# Maps ConsultationNoteTemplateModel fields (using bool) to target dictionary keys.
# NOTE: Dynamic grid/fax checkboxes are excluded.
# NOTE: Grade scales (FD_gs...) are excluded.

CONSULTATION_CHECKBOXES_MAPPING = {  # Corrected
    # Corrected
    # Corrected
    # Corrected
    # Corrected
    # Corrected
    # Corrected
    # Corrected
    # Corrected
    # For PE Chest
    # Single radio treated as bool
    # Single radio treated as bool
    # Modelled as separate bools
    # Single radio treated as bool
    "hm_colonoscopy_enabled": "FD_chkPHHS_Colon",
    "hm_dexascan_enabled": "FD_chkPHHS_Dexascan",
    "sh_living_with_spouse": "FD_chkWithSpouse",
    "sh_living_alone": "FD_chkAlone",
    "sh_living_with_children": "FD_chkWithChildern",
    "sh_living_nursing_home": "FD_chkNrsgHome",
    "sh_living_other_enabled": "FD_chkOther_2",
    "sh_drug_use_type_enabled": "FD_chkSHDrugs",
    "sh_alcohol_drinks_per_day_enabled": "FD_chkSHAlchUse_4",
    "sh_alcohol_drinks_per_week_enabled": "FD_chkSHAlchUse_6",
    "sh_alcohol_drinks_per_month_enabled": "FD_chkSHAlchUse_8",
    "sh_alcohol_drinks_per_year_enabled": "FD_chkSHAlchUse_10",
    "sh_alcohol_stopped_year_enabled": "FD_chkSHAlchStop",
    "sh_tobacco_discontinued_year_enabled": "FD_chkSHTobUse_20",
    "sh_tobacco_pack_years_enabled": "FD_chkSHTobUse_PH",
    "sh_tobacco_type_details_enabled": "FD_chkSHTobUse_KIND",
    "sh_occupational_exposure_none": "FD_chkSHOP_Neg",
    "sh_occupational_exposure_type_enabled": "FD_chkSHOP_TYPE",
    "sh_occupational_exposure_solvent": "FD_chkSolventexposure",
    "sh_occupational_exposure_asbestos": "FD_chkAsbestosExp",
    "sh_occupational_exposure_agent_orange": "FD_chkAgentOrangeexp",
    "ros_general_system_negative": "FD_chkNegative",
    "ros_eyes_system_negative": "FD_chkROSEyes_Neg",
    "ros_enmt_system_negative": "FD_chkROSENMT_Neg",
    "ros_cardiac_system_negative": "FD_chkROSCardiac_Neg",
    "ros_cardiac_raynauds_no": "FD_chkROSCardiac_NR",
    "ros_cardiac_raynauds_yes": "FD_chkROSCardiac_R",
    "ros_resp_system_negative": "FD_chkROSResp_Neg",
    "ros_gi_system_negative": "FD_chkROSGastro_Neg",
    "ros_gu_system_negative": "FD_chkROSGenito_Neg",
    "ros_msk_system_negative": "FD_chkROSSkel_Neg",
    "ros_neuro_system_negative": "FD_chkROSNeuro_Neg",
    "ros_heme_system_negative": "FD_chkROSHema_Neg",
    "ros_endo_system_negative": "FD_chkHLI",
    "ros_endo_no_polydipsia": "FD_chkROSEndo_NP",
    "ros_endo_polydipsia_present": "FD_chkROSEndo_Polydipsia",
    "ros_endo_no_polyphagia": "FD_chkROSEndo_NoP",
    "ros_endo_polyphagia_present": "FD_chkROSEndo_Polyphagia",
    "ros_endo_no_polyuria": "FD_chkROSEndo_NoPolyuria",
    "ros_endo_polyuria_present": "FD_chkROSEndo_Polyuria",
    "pe_general_system_negative": "FD_chkPEGeneral_Neg",
    "pe_head_system_negative": "FD_chkPE_Neg",
    "pe_eyes_system_negative": "FD_chkPEEyes_Neg",
    "pe_eyes_deferred": "FD_chkPEEYES_D",
    "pe_enmt_system_negative": "FD_chkPEENMT_Neg",
    "pe_enmt_tracheostomy_present": "FD_chkPEENMT_22",
    "pe_cardiac_system_negative": "FD_chkPECardiac_Neg",
    "pe_resp_system_negative": "FD_chkPEResp_Neg",
    "pe_respiratory_also_noted_enabled": "FD_chkPEresp_other",
    "pe_gi_system_negative": "FD_chkPEGastro_Neg",
    "pe_abdomen_scars_enabled": "FD_chkScarspresent",
    "pe_heme_system_negative": "FD_chkPEHema_Neg",
    "pe_msk_system_negative": "FD_chkPESkel_Neg",
    "pe_msk_also_noted_enabled": "FD_chkAlsonoted_1",
    "pe_extremities_system_negative": "FD_chkPEExtremities",
    "pe_neuro_system_negative": "FD_chkPENeuro_Neg",
    "pe_rectal_system_negative": "FD_chkPERectal_negative",
    "pe_rectal_deferred": "FD_chkPERectal_Deferred",
    "pe_gu_system_negative": "FD_chkPEGU_02",
    "pe_gu_deferred": "FD_chkPEGU_Deferred",
    "peripheral_smear_normal": "FD_chkNormal PS",
    "peripheral_smear_micro": "FD_chkMicro PS",
    "peripheral_smear_macro": "FD_chkMacro PS",
    "acp_date_of_discussion_enabled": "FD_chkDOD_ACP",
    "pain_tx_reassess": "FD_chknoaction",
    "pain_tx_continue": "FD_chkContinueregimenpain",
    "pain_tx_narcotic_adjusted": "FD_chkNarcoticdoseadjustedpain",
    "pain_tx_narcotic_prescribed": "FD_chkopioids",
    "pain_tx_non_narcotic_adjusted": "FD_chkNonnarcoticadjusted",
    "pain_tx_non_narcotic_prescribed": "FD_chknonnarcoticthisvisit",
    "pain_tx_psych_support": "FD_chkpsychologicalsupport",
    "pain_tx_education": "FD_chkeducate",
    "pain_tx_refer_pain_mgmt": "FD_chkpainmanagement",
    "pain_tx_refused": "FD_chkpainrefused",
    "pain_tx_other_provider": "FD_chkotherdocpain",
    "depression_tx_no_action": "FD_chknoactionneeded",
    "depression_tx_psychotherapy": "FD_chkPsychotherapy",
    "depression_tx_meds_prescribed": "FD_chkprescribedantidepressant",
    "depression_tx_declined_meds": "FD_chkPatientdeclinedmedicationmanagementforme",
    "depression_tx_declined_referral": "FD_chkPatientdeclinedreferraltomentalhealthser",
    "depression_tx_other_provider": "FD_chkOtherprovidermentalhealth",
    "depression_tx_refused": "FD_chkpatientrefused",
    "depression_tx_inaccurate_screen": "FD_chkfunctionalcapacitymotivation",
    "depression_tx_bipolar_excluded": "FD_chkPatienthasbipolardisorderVerifythisisinO",
    "mdm_high_numcomplex_chronic_severe": "FD_chkhigh_1+chronicillnesseswithsevereexacerbation",
    "mdm_high_numcomplex_threat_to_life": "FD_chkhigh_1acuteorchronicillnessorinjurythatposesa",
    "mdm_moderate_numcomplex_chronic_exacerbation": "FD_chkmod_1ormorechronic",
    "mdm_moderate_numcomplex_stable_chronic": "FD_chkmod_2ormorestablechronic",
    "mdm_moderate_numcomplex_undiagnosed_uncertain": "FD_chkmod_1undiagnosednewproblem",
    "mdm_moderate_numcomplex_acute_systemic": "FD_chkmod_1acuteillnesswithsystemicsymptoms",
    "mdm_moderate_numcomplex_acute_complicated": "FD_chkmod_1acutecomplicatedinjury",
    "mdm_low_numcomplex_self_limited_minor": "FD_chklow_2ormoreself-limitedorminorproblems",
    "mdm_low_numcomplex_stable_chronic": "FD_chklow_1stablechronicillness",
    "mdm_low_numcomplex_acute_uncomplicated": "FD_chklow_1acuteuncomplicatedillnessorinjury",
    "mdm_high_cat1_review_notes": "FD_chkhigh_Reviewexternalnotes",
    "mdm_high_cat1_review_test": "FD_chkhigh_reviewtest",
    "mdm_high_cat1_order_test": "FD_chkhigh_Orderingofeachuniquetest",
    "mdm_high_cat1_independent_historian": "FD_chkhigh_assessmentrequiringanindependenthistoria",
    "mdm_high_cat2_independent_interpretation": "FD_chkCategory2Independentinterpretationoftest",
    "mdm_high_cat3_discussion": "FD_chkCategory3Discussionofmanagementortestint",
    "mdm_moderate_cat1_review_notes": "FD_chkmod_Reviewexternalnotes_1",
    "mdm_moderate_cat1_review_test": "FD_chkReviewoftheresultsofeachuniquetest",
    "mdm_moderate_cat1_order_test": "FD_chkmod_ordering",
    "mdm_moderate_cat1_independent_historian": "FD_chkmod_Assessmentrequiringanindependenthistoria",
    "mdm_moderate_cat2_independent_interpretation": "FD_chkmod_cat2",
    "mdm_moderate_cat3_discussion": "FD_chkmod_cat3",
    "mdm_low_amount_tests_docs": "FD_chklow_tests",
    "mdm_low_amount_independent_historian": "FD_chklow_assess",
    "mdm_high_risk_drug_monitoring": "FD_chkDrugtherapyrequiringintensivemonitoringf",
    "mdm_high_risk_elective_major_surgery_risks": "FD_chkDecisionregardingelectivemajorsurgerywit",
    "mdm_high_risk_hospitalization": "FD_chkDecisionregardinghospitalization",
    "mdm_high_risk_dnr_deescalate": "FD_chkDecisionnottoresuscitateortode-escalatec",
    "mdm_moderate_risk_rx_mgmt": "FD_chkmod_rx",
    "mdm_moderate_risk_minor_surgery_risks": "FD_chkmod_minor",
    "mdm_moderate_risk_elective_major_surgery_no_risks": "FD_chkmod_major",
    "mdm_moderate_risk_social_determinants": "FD_chkmod_socialdets",
    "mdm_low_risk": "FD_chkLowrisk",
    "pe_chest_also_noted_enabled": "FD_chkAlsonoted",
    "pe_enmt_nodes_present": "FD_rdoPEENMT_18",
    "pe_gi_ostomy_present": "FD_rdoOstomy present",
    "pe_heme_petechiae_no": "FD_rdoPEHema_25",
    "pe_heme_petechiae_yes": "FD_rdoPEHem_10",
    "pe_heme_purpura_no": "FD_rdoPEHema_26",
    "pe_heme_purpura_yes": "FD_rdoPEHema_14",
    "pe_heme_neck_lymph_no": "FD_rdoPEHema_20",
    "pe_heme_neck_lymph_yes": "FD_rdoPEHema_28",
    "pe_heme_axillary_lymph_no": "FD_rdoPEHema_22",
    "pe_heme_axillary_lymph_yes": "FD_rdoPEHema_30",
    "pe_heme_groin_lymph_no": "FD_rdoPEHema_24",
    "pe_heme_groin_lymph_yes": "FD_rdoPEHema_32",
    "pe_msk_deferred": "FD_rdoPESkel_Deferred",
}
