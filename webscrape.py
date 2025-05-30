from staffspy import LinkedInAccount, SolverType, DriverType, BrowserType

account = LinkedInAccount(
    session_file="session.pkl",
    log_level="1",
)

users = account.scrape_users(
    user_ids=['bennett-carroll-05a0083b', 'bjchin']
)

users.to_csv("staff.csv", index=False)