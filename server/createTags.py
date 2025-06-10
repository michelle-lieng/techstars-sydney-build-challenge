def createTags(is_current_founder=False, ai_in_curr_startup=False, was_prev_founder=False, top_degree_label=None, was_in_accelerator=False,
                was_in_scaleup=False, was_in_bigtech=False, is_migrant=False, is_stealth=False, gender=None):
    tags = []
    if (is_current_founder):
        tags.append("Founder")

    if (was_prev_founder):
        tags.append("Previous Founder")

    if (ai_in_curr_startup):
        tags.append("AI Startup")

    if (top_degree_label):
        tags.append(top_degree_label)
    
    if (was_in_accelerator):
        tags.append("Accelerator Participant")

    if (gender == 'Female') & (is_current_founder):
        tags.append("Female Founder")
    
    if (was_in_scaleup):
        tags.append("Scaleup Alumni")
    
    if (was_in_bigtech):
        tags.append("Worked in Big Tech")
    
    if (is_migrant):
        tags.append("Migrant")

    if (is_stealth):
        tags.append("Building in Stealth")

    return tags