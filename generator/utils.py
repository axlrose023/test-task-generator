from faker import Faker


def fake_data(data_type, from_int, to_int):
    fake = Faker()
    if data_type == "Name":
        fake_data = fake.name()
    elif data_type == "Email":
        fake_data = fake.email()
    elif data_type == "Job":
        fake_data = fake.job()
    elif data_type == "Domain":
        fake_data = fake.domain_name()
    elif data_type == "Phone":
        fake_data = fake.phone_number()
    elif data_type == "Text":
        fake_data = fake.text(max_nb_chars=int(30))
    elif data_type == "Integer":
        fake_data = fake.random_int(min=from_int, max=to_int)
    return fake_data

