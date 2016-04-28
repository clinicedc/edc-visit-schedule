# edc-visit-schedule

Add a data collection schedule to your app.


Process Overview
----------------
Research data is collected on case report forms (CRFs) during a visit. Before
data collection can begin a subject completes the informed consent process.
Before consent and/or after, depending on design, an eligibility checklist is 
completed. Once consented and eligibility confirmed, data collection may begin.

A protocol may define multiple data collection schedules and direct participants
to one or the other based on some inclusion / exclusion criteria. 

We prefer to deliberately "register" a participant to a data collection
schedule. The "registration" model/form may be the same as the eligibility
checklist (administered after the ICF) or a separate model/form to be completed
after the ICF and eligibility checklist.

__edc-visit-schedule__ takes over once the informed consent process is complete.

The module defines:
 
 - visits (model VisitDefinition)
 - data collection schedule (Schedule)
 - a model that registers a participant to a data collection schedule (Member)
 
 Model class "Member" through content_type points to a model/form to be
 completed by the participant. If the model/form saves successfully, the
 participant is considered a member of the schedule group. Scheduled
 appointments will be created for all visits defined in the VisitDefinitions
 associated with the Schedule.
 
 Appointments are part of __edc-appointment__.   