def createTags(is_current_founder=False, ai_in_curr_startup=False, was_prev_founder=False, top_degree_label=None, was_in_accelerator=False,
                was_in_scaleup=False, was_in_bigtech=False, is_migrant=False, is_stealth=False):
    tags = []
    if (is_current_founder or was_prev_founder):
        tags.append("Founder")

    if (ai_in_curr_startup):
        tags.append("AI Founder")

    if (top_degree_label):
        tags.append(top_degree_label)
    
    if (was_in_accelerator):
        tags.append("Accelerator")
    
    if (was_in_scaleup):
        tags.append("Scaleup")
    
    if (was_in_bigtech):
        tags.append("Big Tech")
    
    if (is_migrant):
        tags.append("Migrant")

    if (is_stealth):
        tags.append("Stealth Founder")

    return tags