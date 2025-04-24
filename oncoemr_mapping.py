FOLLOWUP_TEXTFIELDS_MAPPING = {
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


FOLLOWUP_RADIO_BUTTONS_MAPPING = {
    "marital_status": {
        "group_id": "MaritalStatus",  # This is the group identifier in the '%02' suffix
        "options": {
            "Single": "FD_rdoSingle",
            "Married": "FD_rdoMarried",
            "Divorced": "FD_rdoDivorced",
            "Widowed": "FD_rdoWidowed",
            "Has Significant Other": "FD_rdoHasSignificantOther",
        },
    },
    "tobacco_status": {
        "options": {
            "Non Smoker": "FD_rdoARRANonSmoker",
            "Never Smoked": "FD_rdoARRANeverSmoker",
            "Smoker": "FD_rdoARRACurrentSmoker",
            "Ex-Smoker": "FD_rdoARRAFormerSmoker",
        }
    },
    "tobacco_frequency": {
        "options": {
            "Tobacco smoking consumption unknown": "FD_rdoARRAUnknownIfSmoked",
            "Smokes tobacco daily": "FD_rdoARRACurrentEverydaySmoker",
            "Occasional tobacco smoker": "FD_rdoARRACurrentSomeDaySmoker",
        }
    },
    "tobacco_intensity": {
        "options": {
            "Light tobacco smoker": "FD_rdoARRAlighttobaccosmoker",
            "Heavy tobacco smoker": "FD_rdoARRAheavytobaccosmoker",
        }
    },
    "ecigarette_use": {
        "options": {"Electronic cigarette user": "FD_rdoARRAecigarretteuser"}
    },
    "tobacco_type": {
        "options": {
            "Pipe smoker": "FD_rdoARRApipesmoker",
            "Snuff User": "FD_rdoARRASnuffUser",
            "Chews tobacco": "FD_rdoARRAchewstobacco",
            "Use of moist powdered tobacco": "FD_rdoARRAuseofmoistpowderedtobacco",
        }
    },
    "smokeless_tobacco": {
        "options": {
            "Smokeless tobacco NON user": "FD_rdoARRAsmokelessnonuser",
            "User of smokeless tobacco": "FD_rdoARRAuserofsmokelesstobacco",
        }
    },
    "tobacco_exposure": {
        "options": {
            "Exposed to tobacco smoke at home": "FD_rdoARRAexposedathome",
            "Exposed to tobacco smoke at work": "FD_rdoARRAexposedatwork",
            "No known exposure to tobacco smoke": "FD_rdoARRANoKnownExposureToTobaccoSmoke",
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
    "mother_cancer_history": {
        "options": {
            "Has Cancer History": "FD_rdoFHFamCancerMother_Yes",
            "None": "FD_rdoFHFamCancerMother_No",
        }
    },
    "father_cancer_history": {
        "options": {
            "Has Cancer History": "FD_rdoFHFamCancerFather_Yes",
            "None": "FD_rdoFHFamCancerFather_No",
        }
    },
    "siblings_cancer_history": {
        "options": {
            "Has Cancer History": "FD_rdoFHFamCancerSiblings_Yes",
            "None": "FD_rdoFHFamCancerSiblings_No",
        }
    },
    "children_cancer_history": {
        "options": {
            "Has Cancer History": "FD_rdoFHFamCancerChildren_Yes",
            "None": "FD_rdoFHFamCancerChildren_No",
        }
    },
    "other_family_history": {
        "options": {
            True: "FD_rdoFHOtherFamHx",
            False: "",  # No explicit "No" option for other family history
        }
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
    "ros_enmt_hearing": {
        "options": {
            "No Hearing Loss": "FD_rdoROSENMT_NHL",
            "Hearing Loss": "FD_rdoROSENMT_HL",
        }
    },
    "ros_enmt_ringing": {
        "options": {
            "No Ringing in Ears": "FD_rdoROSENMT_NRIE",
            "Ringing in Ears": "FD_rdoROSENMT_RIE",
        }
    },
    "ros_enmt_sinus": {
        "options": {
            "No Sinus Trouble": "FD_rdoROSENMT_NST",
            "Sinus Trouble": "FD_rdoROSENMT_ST",
        }
    },
    "ros_enmt_swallowing": {
        "options": {
            "No Trouble Swallowing": "FD_rdoROSENMT_NTS",
            "Trouble Swallowing": "FD_rdoROSENMT_TS",
        }
    },
    "ros_enmt_throat": {
        "options": {
            "No Sore Throat": "FD_rdoROSENMT_NSOT",
            "Sore Throat": "FD_rdoROSENMT_SOT",
        }
    },
    "ros_enmt_nasal": {
        "options": {
            "No Nasal drainage": "FD_rdoNoNasaldrainage",
            "Nasal drainage": "FD_rdoNasaldrainage",
        }
    },
    "ros_enmt_nosebleeds": {
        "options": {
            "No Nose Bleeds": "FD_rdoROSENMT_NNB",
            "Nose Bleeds": "FD_rdoROSENMT_NB",
        }
    },
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
    "ros_cardiac_leg_swelling": {
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
    "ros_resp_shortness_of_breath": {
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
    "ros_gastro_nausea": {
        "options": {"No Nausea": "FD_rdoROSGastro_NN", "Nausea": "FD_rdoROSGastro_N"}
    },
    "ros_gastro_vomiting": {
        "options": {
            "No Vomiting": "FD_rdoROSGastro_NV",
            "Vomiting": "FD_rdoROSGastro_V",
        }
    },
    "ros_gastro_heartburn": {
        "options": {
            "No Heartburn": "FD_rdoROSGastro_NHB",
            "Heartburn": "FD_rdoROSGastro_HB",
        }
    },
    "ros_gastro_constipation": {
        "options": {
            "No Constipation": "FD_rdoROSGastro_NC",
            "Constipation": "FD_rdoROSGastro_C",
        }
    },
    "ros_gastro_diarrhea": {
        "options": {
            "No Diarrhea": "FD_rdoROSGastro_ND",
            "Diarrhea": "FD_rdoROSGastro_D",
        }
    },
    "ros_gastro_abdominal_pain": {
        "options": {
            "No Abdominal Pain": "FD_rdoROSGastro_NAP",
            "Abdominal Pain": "FD_rdoROSGastro_AP",
        }
    },
    "ros_gastro_rectal_bleeding": {
        "options": {
            "No Rectal Bleeding": "FD_rdoROSGastro_NRB",
            "Rectal Bleeding": "FD_rdoROSGastro_RB",
        }
    },
    "ros_gastro_bowel_incontinence": {
        "options": {
            "No Bowel Incontinence": "FD_rdoROSGastro_NBI",
            "Bowel Incontinence": "FD_rdoROSGastro_BI",
        }
    },
    "ros_genito_burning": {
        "options": {
            "No Burning on Urination": "FD_rdoROSGenito_NBU",
            "Burning on Urination": "FD_rdoROSGenito_BU",
        }
    },
    "ros_genito_pain": {
        "options": {
            "No Pain with Urination": "FD_rdoROSGenito_NPU",
            "Pain with Urination": "FD_rdoROSGenito_PU",
        }
    },
    "ros_genito_urgency": {
        "options": {"No Urgency": "FD_rdoROSGU_NU", "Urgency": "FD_rdoROSGU_U"}
    },
    "ros_genito_blood": {
        "options": {
            "No Blood in Urine": "FD_rdoROSGenito_NBIU",
            "Blood in Urine": "FD_rdoROSGenito_BIU",
        }
    },
    "ros_genito_frequency": {
        "options": {
            "No Frequent Urination": "FD_rdoROSGenito_NFU",
            "Frequent Urination": "FD_rdoROSGenito_FU",
        }
    },
    "ros_genito_incontinence": {
        "options": {
            "No Urinary Incontinence": "FD_rdoROSGenito_NUI",
            "Urinary Incontinence": "FD_rdoROSGenito_UI",
        }
    },
    "ros_skel_muscle_pain": {
        "options": {
            "No Muscle Pain": "FD_rdoROSSkel_NMP",
            "Muscle Pain": "FD_rdoROSSkel_MP",
        }
    },
    "ros_skel_stiffness": {
        "options": {
            "No Stiffness": "FD_rdoROSSkel_NST",
            "Stiffness": "FD_rdoROSSkel_ST",
        }
    },
    "ros_skel_joint_pain": {
        "options": {
            "No Joint Pain": "FD_rdoROSSkel_NJP",
            "Joint Pain": "FD_rdoROSSkel_JP",
        }
    },
    "ros_skel_joint_swelling": {
        "options": {
            "No joint swelling": "FD_rdoNojointswelling",
            "Joint swelling": "FD_rdoJointswelling",
        }
    },
    "ros_skel_back_pain": {
        "options": {
            "No Back Pain": "FD_rdoROSSkel_NBP",
            "Back Pain": "FD_rdoROSSkel_BP",
        }
    },
    "ros_skin_rash": {
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
    "ros_neuro_balance": {
        "options": {
            "No Loss of Balance": "FD_rdoROSNeuro_NLOB",
            "Loss of Balance": "FD_rdoROSNeuro_LOB",
        }
    },
    "ros_neuro_weakness": {
        "options": {
            "No Weakness of Limbs": "FD_rdoROSNeuro_NWOL",
            "Weakness of Limbs": "FD_rdoROSNeuro_WOL",
        }
    },
    "ros_neuro_sensation": {
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
    "ros_neuro_memory": {
        "options": {
            "No Memory Loss": "FD_rdoROSNeuro_NML",
            "Memory Loss": "FD_rdoROSNeuro_ML",
        }
    },
    "ros_neuro_thinking": {
        "options": {
            "No Thinking Difficulty": "FD_rdoROSNeuro_NTD",
            "Thinking Difficulty": "FD_rdoROSNeuro_TD",
        }
    },
    "ros_psyc_system": {
        "options": {"Deferred": "FD_rdoROSPsyc_defer", "System": "FD_rdoROSPsyc_Neg"}
    },
    "ros_psyc_nervousness": {
        "options": {
            "No Nervousness": "FD_rdoROSPsyc_NNER",
            "Nervousness": "FD_rdoROSPsyc_NER",
        }
    },
    "ros_psyc_depression": {
        "options": {
            "No Depression": "FD_rdoROSPsyc_NDEP",
            "Depression": "FD_rdoROSPsyc_DEP",
        }
    },
    "ros_psyc_restlessness": {
        "options": {
            "No restlessness": "FD_rdoNorestlessness",
            "Restless": "FD_rdoRestless",
        }
    },
    "ros_psyc_sleep": {
        "options": {
            "No difficulty sleeping": "FD_rdoNodifficultysleeping",
            "Difficulty sleeping": "FD_rdoDifficultysleeping",
        }
    },
    "ros_hema_bruising": {
        "options": {"No bruising": "FD_rdoNObruising", "Bruising": "FD_rdoBruising"}
    },
    "ros_hema_bleeding": {
        "options": {"No Bleeding": "FD_rdoNoBleeding_1", "Bleeding": "FD_rdoBleeding_1"}
    },
    "ros_hema_armpits": {
        "options": {
            "No Lumps in Arm Pits": "FD_rdoROSHema_NAL",
            "Lumps in Arm Pits": "FD_rdoROSHema_AL",
        }
    },
    "ros_hema_neck": {
        "options": {
            "No Lumps in Neck": "FD_rdoROSHema_NN",
            "Lumps in Neck": "FD_rdoROSHema_N",
        }
    },
    "ros_hema_groin": {
        "options": {
            "No Lumps in Groin": "FD_rdoROSHema_NG",
            "Lumps in Groin": "FD_rdoROSHema_G",
        }
    },
    "physical_exam_chaperone": {
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
    "pe_general_age": {
        "options": {
            "Appears Stated age": "FD_rdoPEGeneral_14",
            "Elderly appearance": "FD_rdoPEGeneral_16",
        }
    },
    "pe_head_not_assessed": {"options": {True: "FD_rdoNotassessed"}},
    "pe_head_trauma": {
        "options": {
            "Atraumatic and normocephalic": "FD_rdoAtraumaticandnormocephalic",
            "Traumatic with a wound/scar on the scalp/face": "FD_rdoTraumaticwithawoundscaronthescalpface",
        }
    },
    "pe_eyes_pupils": {
        "options": {"PERRLA": "FD_rdoPEEyes_02", "Unequal": "FD_rdoPEEyes_04"}
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
    "pe_eyes_conjunctiva": {
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
    "pe_enmt_lymph": {
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
    "pe_enmt_oral": {
        "options": {
            "No oral lesions": "FD_rdoNoorallesions",
            "Oral abnormality(ies) as noted": "FD_rdoOralabnormalityiesasnoted",
        }
    },
    "pe_cardiac_s12": {
        "options": {
            "S1, S2 no mumurs": "FD_rdoPECardiac_02",
            "S1, S2 mumurs present.": "FD_rdoPECardiac_04",
        }
    },
    "pe_cardiac_s34": {
        "options": {
            "S3,S4 no gallop": "FD_rdoPECardiac_06",
            "S3/S4 gallop present": "FD_rdoPECardiac_08",
        }
    },
    "pe_cardiac_rubs": {
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
    "pe_cardiac_radial": {
        "options": {
            "Radial Pulse Present": "FD_rdoRadialPulsePresent",
            "Radial pulses absent": "FD_rdoRadialpulsesabsent",
        }
    },
    "pe_cardiac_femoral": {
        "options": {
            "Femoral Pulses present": "FD_rdoPECardiac_22",
            "Femoral pulses absent": "FD_rdoPECardiac_24",
        }
    },
    "pe_cardiac_pedal": {
        "options": {
            "Pedal Pulses present": "FD_rdoPedalPulsespresent",
            "Pedal Pulses absent": "FD_rdoPedalPulsesabsent",
        }
    },
    "pe_chest_symmetry": {
        "options": {
            "Symmetrical": "FD_rdoSymeterical",
            "Asymmetrical": "FD_rdoAsymmetrical",
        }
    },
    "pe_chest_kyphosis": {
        "options": {"No kyphosis": "FD_rdoNokyphosis", "Kyphosis": "FD_rdoKyphosis"}
    },
    "pe_chest_scoliosis": {
        "options": {
            "No scoliosis": "FD_rdoNoscoleosis",
            "Scoliosis noted": "FD_rdoScoleosisnoted",
        }
    },
    "pe_resp_lung_sounds": {
        "options": {
            "Clear, No rales/Rhonchi": "FD_rdoPEResp_02",
            "Rales/Rhonchi present": "FD_rdoPEResp_04",
            "Pleural Effusion": "FD_rdoPEResp_06",
        }
    },
    "pe_resp_percussion": {
        "options": {
            "Percussion and palpation-Normal": "FD_rdoPercussionandpalpation",
            "Percussion and palpation abnormal": "FD_rdoPercussionandpalpationabnormal",
        }
    },
    "pe_abdomen_consistency": {
        "options": {
            "Abdomen soft": "FD_rdoPEAbdomen_20",
            "Abdomen firmness": "FD_rdoPEAbdomen_21",
        }
    },
    "pe_abdomen_tenderness": {
        "options": {
            "Abdomen non-tender": "FD_rdoPEAbdomen_22",
            "Abdomen Tender": "FD_rdoPEAbdomen_25",
        }
    },
    "pe_abdomen_distension": {
        "options": {
            "Abdomen non-distended": "FD_rdoPEAbdomen_23",
            "Abdomen Distended": "FD_rdoPEAbdomen_27",
        }
    },
    "pe_abdomen_masses": {
        "options": {
            "Abdomen without masses": "FD_rdoPEAbdomen_24",
            "Abdomen Mass(es)": "FD_rdoPEAbdomen_29",
        }
    },
    "pe_abdomen_ascites": {
        "options": {"No Ascites": "FD_rdoPEAbdomen_32", "Ascites": "FD_rdoPEAbdomen_26"}
    },
    "pe_abdomen_hepatomegaly": {
        "options": {
            "No hepatomegaly": "FD_rdoPEAbdomen_NoHepato",
            "Hepatomegaly": "FD_rdoPEAbdomen_Hepato",
        }
    },
    "pe_abdomen_splenomegaly": {
        "options": {
            "No splenomegaly": "FD_rdoPEAbdomen_NoSpleno",
            "Splenomegaly": "FD_rdoPEAbdomen_Spleno",
        }
    },
    "pe_abdomen_hernia": {
        "options": {"No hernia": "FD_rdoNohernia", "Hernia": "FD_rdoHernia"}
    },
    "pe_abdomen_bowel_sounds": {
        "options": {
            "Bowel sounds -Normal": "FD_rdoBowelsounds-Normal",
            "Bowel sounds -abnormal": "FD_rdoBowelsounds-abnormal",
        }
    },
    "pe_abdomen_ostomy": {"options": {True: "FD_rdoOstomy present"}},
    "pe_musculoskeletal_status": {
        "options": {
            "Deferred": "FD_rdoPESkel_Deferred",
            # Add other options here if they share the name="FD_rdoNEG"
        }
    },
    "pe_musculoskeletal_gait": {
        "options": {
            "Normal gait and station": "FD_rdoPESkel_23",
            "Abnormal gait and station": "FD_rdoPESkel_24",
        }
    },
    "pe_musculoskeletal_rom": {
        "options": {
            "Range of motion normal": "FD_rdoPESkel_26",
            "Decreased range of motion": "FD_rdoPESkel_28",
        }
    },
    "pe_musculoskeletal_tone": {
        "options": {
            "Strength/Tone normal": "FD_rdoPESkel_30",
            "Strength/Tone decreased": "FD_rdoPESkel_32",
        }
    },
    "pe_musculoskeletal_stature": {
        "options": {
            "Stature Normal": "FD_rdoPESkel_34",
            "Loss of Stature": "FD_rdoPESkel_36",
        }
    },
    "pe_extremities_status": {
        "options": {
            "Not examined": "FD_rdoNotexamined"
            # Add others if they share name="FD_rdoOOH_Dz554031187_3458"
        }
    },
    "pe_extremities_edema": {
        "options": {
            "Edema-None": "FD_rdoEdema-None",
            "Edema Present": "FD_rdoEdemapresent",  # Target key is the radio button value/id
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
    "pe_neurologic_alertness": {
        "options": {
            "Alert and Oriented": "FD_rdoAlertandOriented",
            "Altered orientation/alertness": "FD_rdoAlertedorientationalertness",
        }
    },
    "pe_neurologic_speech": {
        "options": {
            "Normal Speech": "FD_rdoNormalSpeech",
            "Abnormal Speech": "FD_rdoAbnormalSpeech",  # Target key is the radio button value/id
        }
    },
    "pe_neurologic_hemiplegia": {
        "options": {
            "No hemiplegia": "FD_rdoPENeurologic_24",
            "Hemiplegia": "FD_rdoPENeurologic_26",
        }
    },
    "pe_neurologic_hemiparesis": {
        "options": {
            "No hemiparesis": "FD_rdoNohemiparesis",
            "Hemiparesis": "FD_rdoHemiparesis",
        }
    },
    "pe_neurologic_cranial_nerves": {
        "options": {
            "Cranial nerves intact": "FD_rdoPENeurologic_28",
            "Paralysis cranial nerves": "FD_rdoPENeurologic_30",
        }
    },
    "pe_neurologic_sensory": {
        "options": {
            "No sensory deficits": "FD_rdoPENeurologic_32",
            "Sensory deficits": "FD_rdoPENeurologic_34",
        }
    },
    "pe_neurologic_motor": {
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
            "30 min (99214)": "FD_rdoLenPtVisit_04",
            "39 min (99214)": "FD_rdoLenPtVisit_02",
            "40 min (99215)": "FD_rdoLenPtVisit_03",
            "54 min (99215)": "FD_rdoLenPtVisit_08",
            "Other": "FD_rdoOther_1",  # Target key is the radio button value/id
        }
    },
    "sh_drug_use_status": {
        "options": {"Negative": "FD_rdoSHDrugs_Neg", "Positive": "FD_rdoSHDrugs_Pos"}
    },
    "sh_alcohol_use_status": {
        "options": {
            "Not Asked": "FD_rdoSHAlchUse_NE",
            "Never": "FD_rdoSHAlchUse_Neg",
            "Currently uses": "FD_rdoCurrentlyuses",
            "Former use": "FD_rdoFormeruse",
        }
    },
}


# Define checkbox mappings
FOLLOWUP_CHECKBOXES_MAPPING = {
    "ros_system_negative": "FD_chkNegative",
    "ros_eyes_negative": "FD_chkROSEyes_Neg",
    "ros_enmt_negative": "FD_chkROSENMT_Neg",
    "ros_enmt_hoarseness": "FD_rdoROSENMT_H",
    "ros_cardiac_raynauds": "FD_chkROSCardiac_R",
    "ros_resp_negative": "FD_chkROSResp_Neg",
    "ros_gastro_negative": "FD_chkROSGastro_Neg",
    "ros_genito_negative": "FD_chkROSGenito_Neg",
    "ros_skel_negative": "FD_chkROSSkel_Neg",
    "ros_neuro_negative": "FD_chkROSNeuro_Neg",
    "ros_hema_negative": "FD_chkROSHema_Neg",
    "ros_endo_system": "FD_chkHLI",
    "ros_endo_no_polydipsia": "FD_chkROSEndo_NP",
    "ros_endo_polydipsia": "FD_chkROSEndo_Polydipsia",
    "ros_endo_no_polyphagia": "FD_chkROSEndo_NoP",
    "ros_endo_polyphagia": "FD_chkROSEndo_Polyphagia",
    "ros_endo_no_polyuria": "FD_chkROSEndo_NoPolyuria",
    "ros_endo_polyuria": "FD_chkROSEndo_Polyuria",
    "treatment_reassess_next_visit": "FD_chknoaction",
    "treatment_continue_pain_regimen": "FD_chkContinueregimenpain",
    "treatment_narcotic_dose_adjusted": "FD_chkNarcoticdoseadjustedpain",
    "treatment_narcotic_prescribed": "FD_chkopioids",
    "treatment_nonnarcotic_dose_adjusted": "FD_chkNonnarcoticadjusted",
    "treatment_nonnarcotic_prescribed": "FD_chknonnarcoticthisvisit",
    "treatment_psychological_support": "FD_chkpsychologicalsupport",
    "treatment_patient_education": "FD_chkeducate",
    "treatment_refer_pain_management": "FD_chkpainmanagement",
    "treatment_patient_refused": "FD_chkpainrefused",
    "treatment_other_provider_pain": "FD_chkotherdocpain",
    "depression_no_action_needed": "FD_chknoactionneeded",
    "depression_referral_placed": "FD_chkPsychotherapy",
    "depression_medication_prescribed": "FD_chkprescribedantidepressant",
    "depression_declined_medication": "FD_chkPatientdeclinedmedicationmanagementforme",
    "depression_declined_referral": "FD_chkPatientdeclinedreferraltomentalhealthser",
    "depression_other_provider": "FD_chkOtherprovidermentalhealth",
    "depression_patient_refused": "FD_chkpatientrefused",
    "depression_functional_capacity": "FD_chkfunctionalcapacitymotivation",
    "depression_bipolar_excluded": "FD_chkPatienthasbipolardisorderVerifythisisinO",
    "pe_general_negative": "FD_chkPEGeneral_Neg",
    "pe_head_negative": "FD_chkPE_Neg",
    "pe_eyes_negative": "FD_chkPEEyes_Neg",
    "pe_eyes_deferred": "FD_chkPEEYES_D",
    "pe_enmt_negative": "FD_chkPEENMT_Neg",
    "pe_enmt_nodes": "FD_rdoPEENMT_18",
    "pe_enmt_tracheostomy": "FD_chkPEENMT_22",
    "pe_cardiac_negative": "FD_chkPECardiac_Neg",
    "pe_chest_negative": "FD_chkPEChest_Neg",
    "pe_chest_also_noted": "FD_chkAlsonoted",
    "pe_resp_negative": "FD_chkPEResp_Neg",
    "pe_resp_also_noted": "FD_chkPEresp_other",
    "pe_abdomen_negative": "FD_chkPEGastro_Neg",
    "pe_abdomen_scars_present": "FD_chkScarspresent",
    # "pe_musculoskeletal_also_noted_details": "FD_itbAlsonoted_1",
    "pe_musculoskeletal_system_negative": "FD_chkPESkel_Neg",
    "pe_musculoskeletal_also_noted_enabled": "FD_chkAlsonoted_1",
    "pe_extremities_system_negative": "FD_chkPEExtremities",
    "pe_neurologic_system_negative": "FD_chkPENeuro_Neg",
    "pe_rectal_system_negative": "FD_chkPERectal_negative",
    "pe_rectal_deferred": "FD_chkPERectal_Deferred",
    "pe_gu_system_negative": "FD_chkPEGU_02",
    "pe_gu_deferred": "FD_chkPEGU_Deferred",
    "pe_peripheral_smear_normal": "FD_chkNormal PS",
    "pe_peripheral_smear_micro": "FD_chkMicro PS",
    "pe_peripheral_smear_macro": "FD_chkMacro PS",
    "acp_date_of_discussion_enabled": "FD_chkDOD_ACP",
    # --- NEW Checkbox Mappings (Social History - Occupational Exposure) ---
    "sh_occupational_exposure_none": "FD_chkSHOP_Neg",
    "sh_occupational_exposure_type_enabled": "FD_chkSHOP_TYPE",
    "sh_occupational_exposure_solvent": "FD_chkSolventexposure",
    "sh_occupational_exposure_asbestos": "FD_chkAsbestosExp",
    "sh_occupational_exposure_agent_orange": "FD_chkAgentOrangeexp",
    "sh_drug_use_type_enabled": "FD_chkSHDrugs",
    "sh_alcohol_drinks_per_day_enabled": "FD_chkSHAlchUse_4",  # Target key is checkbox value/id
    "sh_alcohol_drinks_per_week_enabled": "FD_chkSHAlchUse_6",  # Target key is checkbox value/id
    "sh_alcohol_drinks_per_month_enabled": "FD_chkSHAlchUse_8",  # Target key is checkbox value/id
    "sh_alcohol_drinks_per_year_enabled": "FD_chkSHAlchUse_10",  # Target key is checkbox value/id
    "sh_alcohol_stopped_year_enabled": "FD_chkSHAlchStop",
    "sh_tobacco_discontinued_year_enabled": "FD_chkSHTobUse_20",  # Target key is checkbox value/id
    "sh_tobacco_pack_years_enabled": "FD_chkSHTobUse_PH",  # Target key is checkbox value/id
    "sh_tobacco_type_details_enabled": "FD_chkSHTobUse_KIND",
    "sh_living_with_spouse": "FD_chkWithSpouse",  # Target key is checkbox value/id
    "sh_living_alone": "FD_chkAlone",  # Target key is checkbox value/id
    "sh_living_with_children": "FD_chkWithChildern",  # Target key is checkbox value/id
    "sh_living_nursing_home": "FD_chkNrsgHome",  # Target key is checkbox value/id
    "sh_living_other_enabled": "FD_chkOther_2",
    "hm_colonoscopy_enabled": "FD_chkPHHS_Colon",  # Target key is checkbox value/id
    "hm_dexascan_enabled": "FD_chkPHHS_Dexascan",
}
