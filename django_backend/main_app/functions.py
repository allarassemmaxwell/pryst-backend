import random
import string





# GENERATE RANDOM STRING FOR OUTLET
def random_string_generate_outlet_id(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





# GENERATE RANDOM STRING FOR ARTICLE
def random_string_generate_article_number(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





# GENERATE RANDOM STRING FOR PROFILE
def random_string_generate_profile_slug(size=15, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




# GENERATE RANDOM STRING FOR AUDIT
def random_string_generate_audit_slug(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# GENERATE UNIQUE OUTLET ID 
def unique_outlet_id_generator(instance):
    order_new_id= random_string_generate_outlet_id()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(outlet_id= order_new_id).exists()
    if qs_exists:
        return unique_outlet_id_generator(instance)
    return order_new_id




# GENERATE UNIQUE ARTICLE NUMBER 
def unique_article_number_generator(instance):
    order_new_id= random_string_generate_article_number()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(article_number= order_new_id).exists()
    if qs_exists:
        return unique_article_number_generator(instance)
    return order_new_id





# GENERATE UNIQUE PROFILE SLUG 
def unique_profile_slug_generator(instance):
    order_new_id= random_string_generate_profile_slug()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(slug = order_new_id).exists()
    if qs_exists:
        return unique_profile_slug_generator(instance)
    return order_new_id






# GENERATE UNIQUE AUDIT SLUG 
def unique_audit_slug_generator(instance):
    order_new_id= random_string_generate_audit_slug()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(slug = order_new_id).exists()
    if qs_exists:
        return unique_audit_slug_generator(instance)
    return order_new_id






# CLEAN DATA
def clean_data(data):
	if data is None or data == '' or data == 'undefined' or data == 'null':
		cleaned_data = ''
	else:
		cleaned_data = data.strip()
	return cleaned_data