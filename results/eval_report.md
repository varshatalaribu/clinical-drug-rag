# Evaluation report

36 questions (33 answerable, 3 unanswerable)

## Retrieval

| Setting | Hit@1 | Hit@3 | Hit@5 | MRR |
|---|---|---|---|---|
| Vector search only | 63.6% | 84.8% | 87.9% | 0.745 |
| + drug-name filter | 69.7% | 87.9% | 90.9% | 0.790 |
| + drug filter + section boost | 90.9% | 97.0% | 100.0% | 0.945 |

### Questions not answered by the #1 chunk (full system)

- #3 Who should not take Lipitor? (correct rank: 5; top 3: atorvastatin/Indications and Usage, atorvastatin/Warnings and Precautions, atorvastatin/Warnings and Precautions)
- #25 Does azithromycin affect heart rhythm? (correct rank: 2; top 3: azithromycin/Adverse Reactions, azithromycin/Warnings and Precautions, azithromycin/Adverse Reactions)
- #33 Which medication carries a boxed warning about tendon rupture? (correct rank: 2; top 3: metoprolol/Boxed Warning, ciprofloxacin/Boxed Warning, ciprofloxacin/Boxed Warning)

## Answers

| Metric | Score |
|---|---|
| Keyword accuracy (answer contains expected facts) | 97.0% |
| Wrongly refused (answerable but said 'not in label') | 0.0% |
| Citations (of non-refused answers) | 97.0% |
| Faithfulness (LLM judge: all claims supported by source) | 100.0% |
| Refusal accuracy on unanswerable questions | 100.0% |

## Per-question details

**#1 What is the boxed warning for warfarin?** — keywords=OK faithful=True

> The boxed warning for warfarin states that warfarin sodium can cause major or fatal bleeding, and regular monitoring of the INR must be performed in all treated patients [1]. Drugs, dietary changes, and other factors affect the INR levels achieved with warfarin therapy [1]. Patients should be instructed about prevention measures to minimize the risk of bleeding and to report signs and symptoms of bleeding [1].

**#2 What serious metabolic complication does the metformin boxed warning describe?** — keywords=OK faithful=True

> The metformin boxed warning describes lactic acidosis [1][2][3].

**#3 Who should not take Lipitor?** — keywords=OK faithful=True

> Patients with acute liver failure or decompensated cirrhosis, or those with hypersensitivity to atorvastatin or any excipients in atorvastatin calcium tablets, should not take Lipitor [5]. Additionally, concomitant use of cyclosporine, gemfibrozil, tipranavir plus ritonavir, or glecaprevir plus pibrentasvir with atorvastatin calcium is not recommended [2].

**#4 Can lisinopril be used during pregnancy?** — keywords=OK faithful=True

> Use of drugs that act on the renin-angiotensin system during the second and third trimesters of pregnancy reduces fetal renal function and increases fetal and neonatal morbidity and death [2][3]. When pregnancy is detected, discontinue Lisinopril as soon as possible [2][3]. In the unusual case that there is no appropriate alternative, apprise the mother of the potential risk to the fetus and perform serial ultrasound examinations to assess the intra-amniotic environment [1][2]. If oligohydramnios is observed, discontinue Lisinopril unless it is considered lifesaving for the mother [1][4].

**#5 Is there an interaction between clopidogrel and omeprazole?** — keywords=MISS faithful=True

> Yes, there is an interaction between clopidogrel and omeprazole [1][3][5]. Concomitant use of omeprazole (such as omeprazole 80 mg) results in reduced plasma concentrations of clopidogrel's active metabolite and a reduction in platelet inhibition [1][3]. Omeprazole significantly reduces the antiplatelet activity of clopidogrel when given concomitantly or 12 hours apart [1]. Concomitant use with omeprazole should be avoided, and alternative anti-platelet therapy should be considered [3][5].

**#6 What does the boxed warning for Zoloft say about young patients?** — keywords=OK faithful=True

> The boxed warning states that antidepressants increased the risk of suicidal thoughts and behavior in pediatric and young adult patients in short-term studies [1]. All antidepressant-treated patients must be closely monitored for clinical worsening, and for the emergence of suicidal thoughts and behaviors [1].

**#7 What is the usual starting dose of amlodipine for hypertension in adults?** — keywords=OK faithful=True

> The usual initial antihypertensive oral dose of Amlodipine besylate tablets for adults is 5 mg once daily [1]. Small, fragile, elderly patients, or those with hepatic insufficiency may be started on 2.5 mg once daily [1].

**#8 Can levothyroxine be used for weight loss?** — keywords=OK faithful=True

> No, levothyroxine should not be used for the treatment of obesity or for weight loss [1]. In euthyroid patients, doses within the range of daily hormonal requirements are ineffective for weight reduction, and larger doses may produce serious or even life-threatening toxicity [1].

**#9 What musculoskeletal risk is in the ciprofloxacin boxed warning?** — keywords=OK faithful=True

> The ciprofloxacin boxed warning includes tendinitis and tendon rupture as serious musculoskeletal adverse reactions [1][2][3].

**#10 What are the most common side effects of gabapentin?** — keywords=OK faithful=True

> The most common adverse reactions for gabapentin (incidence $\ge$8% and at least twice that for placebo) are:

* **Postherpetic neuralgia:** Dizziness, somnolence, and peripheral edema [4].
* **Epilepsy in patients >12 years of age:** Somnolence, dizziness, ataxia, fatigue, and nystagmus [3][4].
* **Epilepsy in pediatric patients 3 to 12 years of age:** Viral infection, fever, nausea and/or vomiting, somnolence, and hostility [3][4].

**#11 What happens if a patient stops Eliquis early?** — keywords=OK faithful=True

> Premature discontinuation of any oral anticoagulant, including apixaban, increases the risk of thrombotic events [1][2]. To reduce this risk, consider coverage with another anticoagulant if apixaban is discontinued for a reason other than pathological bleeding or completion of a course of therapy [1][2].

**#12 How does omeprazole work?** — keywords=OK faithful=True

> Omeprazole belongs to the substituted benzimidazoles class of antisecretory compounds [1][3]. It suppresses gastric acid secretion by specifically inhibiting the H+/K+ ATPase enzyme system, which is the acid (proton) pump located at the secretory surface of the gastric parietal cell [1][3]. By blocking this enzyme system, omeprazole blocks the final step of acid production [1][3]. This antisecretory effect is dose-related and inhibits both basal and stimulated acid secretion regardless of the stimulus [1][3].

**#13 What serious psychiatric events are warned about for Singulair?** — keywords=OK faithful=True

> Serious neuropsychiatric events reported with montelukast sodium include agitation, aggressive behavior or hostility, anxiousness, depression, disorientation, disturbance in attention, dream abnormalities, dysphemia (stuttering), hallucinations, insomnia, irritability, memory impairment, obsessive-compulsive symptoms, restlessness, somnambulism, suicidal thoughts and behavior (including suicide), tic, and tremor [1][2].

**#14 Which drugs are contraindicated with simvastatin?** — keywords=OK faithful=True

> Simvastatin is contraindicated with the concomitant administration of strong CYP3A4 inhibitors (such as itraconazole, ketoconazole, posaconazole, voriconazole, HIV protease inhibitors, boceprevir, telaprevir, erythromycin, clarithromycin, telithromycin, nefazodone, and cobicistat-containing products) [1]. Simvastatin is also contraindicated with the concomitant administration of gemfibrozil, cyclosporine, or danazol [1].

**#15 What are the signs of furosemide overdose?** — keywords=OK faithful=True

> The principal signs and symptoms of a furosemide overdose are dehydration, blood volume reduction, hypotension, electrolyte imbalance, hypokalemia, and hypochloremic alkalosis, which are extensions of the drug's diuretic action [1].

**#16 What risks are listed in the tramadol boxed warning?** — keywords=OK faithful=True

> The risks listed in the tramadol boxed warning include:

* **Addiction, Abuse and Misuse:** Exposure to tramadol hydrochloride tablets carries risks of addiction, abuse, and misuse, which can lead to overdose and death [1].
* **Life-Threatening Respiratory Depression:** Serious, life-threatening, or fatal respiratory depression may occur, particularly during initiation or after a dosage increase [1]. Life-threatening respiratory depression and death have also occurred in children receiving tramadol [2][3].
* **Accidental Ingestion:** Accidental ingestion of even one dose, especially by children, can cause a fatal overdose [1][4].
* **Risks From Concomitant Use With Benzodiazepines or Other CNS Depressants:** Concomitant use with benzodiazepines or other CNS depressants (including alcohol) may lead to profound sedation, respiratory depression, coma, and death [4][5].
* **Neonatal Opioid Withdrawal Syndrome (NOWS):** Extended use of opioids during pregnancy can result in Neonatal Opioid Withdrawal Syndrome, which may be life-threatening if unrecognized and untreated [4][5].

**#17 What is the risk of taking Xanax together with opioids?** — keywords=OK faithful=True

> The concomitant use of alprazolam and opioids increases the risk of respiratory depression and drug-related mortality, and can lead to overdose or death [1][2][4][5].

**#18 What skin reaction does the lamotrigine boxed warning describe?** — keywords=OK faithful=True

> Lamotrigine can cause life-threatening serious rashes, including Stevens-Johnson syndrome and toxic epidermal necrolysis, and/or rash-related death [1][2]. It can also cause serious rashes requiring hospitalization and discontinuation of treatment [3]. Benign rashes are also caused by lamotrigine, but it is not possible to predict which rashes will prove to be serious or life-threatening [1][2].

**#19 What infections is amoxicillin indicated to treat?** — keywords=OK faithful=True

> Amoxicillin is indicated for the treatment of infections due to susceptible strains of designated microorganisms in adults and pediatric patients, including:
- Upper respiratory tract infections of the ear, nose, and throat [1][2].
- Infections of the genitourinary tract [1][2].
- Infections of the skin and skin structure [1][2].
- Infections of the lower respiratory tract [2][4].

Additionally, in adult patients only, amoxicillin is indicated for:
- *Helicobacter pylori* infection and duodenal ulcer disease (active or 1-year history of a duodenal ulcer) as triple therapy with clarithromycin and lansoprazole, or as dual therapy with lansoprazole delayed-release capsules [2][4][5].

**#20 What is the maximum recommended daily dose of citalopram?** — keywords=OK faithful=True

> The maximum recommended dosage of citalopram is 40 mg once daily [1]. Dosages above 40 mg once daily are not recommended due to the risk of QT prolongation [1]. For patients greater than 60 years of age, patients with hepatic impairment, CYP2C19 poor metabolizers, and patients concomitantly using a CYP2C19 inhibitor, the maximum recommended dosage is 20 mg once daily [1][2][3].

**#21 What does the spironolactone label say about potassium levels?** — keywords=OK faithful=True

> Spironolactone tablets can cause hyperkalemia [3][5]. This risk is increased by impaired renal function, concomitant potassium supplementation, potassium-containing salt substitutes, a diet rich in potassium, or drugs that increase potassium [3][5]. 

Examples of drugs that can increase potassium include:
- ACE inhibitors [2][3][5]
- Angiotensin receptor blockers (ARBs) / angiotensin II antagonists [2][3][5]
- Non-steroidal anti-inflammatory drugs (NSAIDs) [2][5]
- Heparin and low molecular weight heparin [2][5]
- Trimethoprim [2]

Serum potassium levels should be monitored within 1 week of initiation or titration of spironolactone tablets, regularly thereafter, and when ACE inhibitor or ARB therapy is altered [1][3]. More frequent monitoring may be needed if spironolactone is given with other drugs that cause hyperkalemia or in patients with impaired renal function [3]. In heart failure patients who start spironolactone, potassium supplementation should generally be discontinued [1]. If hyperkalemia occurs, the dose should be decreased or spironolactone discontinued and the hyperkalemia treated [3]. Concomitant use with cholestyramine has also been reported to cause hyperkalemic metabolic acidosis [1].

**#22 Should ibuprofen be avoided in later pregnancy?** — keywords=OK faithful=True

> Yes, ibuprofen should be avoided in women at about 30 weeks gestation and later in pregnancy because NSAIDs can cause premature closure of the fetal ductus arteriosus [1][4].

**#23 What liver warning applies to acetaminophen?** — keywords=OK faithful=True

> Severe liver damage may occur if you take more than 4,000 mg of acetaminophen in 24 hours, take it with other drugs containing acetaminophen, or consume 3 or more alcoholic drinks every day while using this product [2]. Additionally, you should ask a doctor before use if you have liver disease [1][2].

**#24 Why should doxycycline generally be avoided in children under 8?** — keywords=OK faithful=True

> Doxycycline should be used in pediatric patients 8 years of age or less only when potential benefits are expected to outweigh risks in severe or life-threatening conditions (such as anthrax or Rocky Mountain spotted fever), particularly when alternative therapies are absent, due to the effects of tetracycline-class drugs on tooth development and growth.

**#25 Does azithromycin affect heart rhythm?** — keywords=OK faithful=True

> Yes, azithromycin can affect heart rhythm [5]. Postmarketing reports include arrhythmias (such as ventricular tachycardia), QT prolongation, torsades de pointes, and cardiovascular death [5]. Additionally, elderly patients or those with proarrhythmic conditions (such as uncorrected hypokalemia or hypomagnesemia, and clinically significant bradycardia) or patients receiving Class IA or Class III antiarrhythmic agents may be more susceptible to drug-associated effects on the QT interval [2].

**#26 What happens if metoprolol is stopped suddenly?** — keywords=OK faithful=True

> Following abrupt cessation of therapy with beta-blocking agents, exacerbations of angina pectoris and, in some cases, myocardial infarction have occurred [1][2][3].

**#27 How does prednisone affect the risk of infection?** — keywords=OK faithful=True

> Prednisone suppresses the immune system and increases the risk of infection with any pathogen, including viral, bacterial, fungal, protozoan, or helminthic pathogens [1]. Specifically, corticosteroids can reduce resistance to new infections, exacerbate existing infections, increase the risk of disseminated infections, increase the risk of reactivation or exacerbation of latent infections, and mask some signs of infection [1]. Infectious complications can range from mild to severe and at times fatal, with the rate of complications increasing alongside increasing corticosteroid dosages [1]. Additionally, if used to treat patients with latent tuberculosis or tuberculin reactivity, reactivation of tuberculosis may occur [1].

**#28 What conditions is Lexapro approved for?** — keywords=OK faithful=True

> Lexapro (escitalopram) tablets are indicated for the treatment of major depressive disorder (MDD) in adults and pediatric patients 12 years of age and older, and generalized anxiety disorder (GAD) in adults [1].

**#29 Is a different rosuvastatin starting dose recommended for Asian patients?** — keywords=OK faithful=True

> Yes, for Asian patients, consider initiation of rosuvastatin therapy with 5 mg once daily due to increased rosuvastatin plasma concentrations [2][3].

**#30 What breathing-related warning is on the albuterol label?** — keywords=OK faithful=True

> Albuterol Sulfate HFA can produce life-threatening paradoxical bronchospasm, which frequently occurs with the first use of a new canister [4]. If paradoxical bronchospasm occurs, the drug should be discontinued immediately and alternative therapy instituted [4]. Additionally, the need for more doses than usual may be a sign of asthma deterioration and requires reevaluation of the treatment regimen [4]. Excessive use of inhaled sympathomimetic drugs in patients with asthma has also been reported in association with fatalities [2]. Finally, immediate hypersensitivity reactions, including bronchospasm, may occur [1].

**#31 In which patients is hydrochlorothiazide contraindicated?** — keywords=OK faithful=True

> Hydrochlorothiazide is contraindicated in patients with anuria, as well as in patients with a hypersensitivity to hydrochlorothiazide or other sulfonamide derived drugs [1].

**#32 Can losartan be combined with aliskiren in patients with diabetes?** — keywords=OK faithful=True

> No, do not coadminister aliskiren with losartan potassium tablets in patients with diabetes, as it is contraindicated [1][3].

**#33 Which medication carries a boxed warning about tendon rupture?** — keywords=OK faithful=True

> Ciprofloxacin carries a boxed warning about tendon rupture [2][3][4].

**#34 How much does Eliquis cost per month?** — refused OK

> The retrieved FDA label sections do not contain this information.

**#35 What is the best restaurant near the metformin manufacturing plant?** — refused OK

> The retrieved FDA label sections do not contain this information.

**#36 What color is the warfarin 7.5 mg tablet's packaging box?** — refused OK

> The retrieved FDA label sections do not contain this information.

