from django.core.validators import RegexValidator

MOBILE_NUMBER_VALIDATOR = RegexValidator(
    r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', 'أدخل رقم هاتف جوال'
)

TELEPHONE_VALIDATOR = RegexValidator(
    r'^([0-9]{3}[-]?)?[0-9]{7}$', 'أدخل رقم هاتف أرضي'
)

GENDER_CHOICES = [
    ('male', 'ذكر'),
    ('female', 'أنثى')
]

MARITAL_CHOICES = [
    ('married', 'متزوج'),
    ('unmarried', 'أعزب')
]

MILITARY_SITUATION_CHOICES = [
    ('delayed', 'مؤجل'),
    ('laid off', 'مسرح')
]

ADJECTIVE_CHOICES = [
    ('demonstrator', 'معيد'), 
    ('returning', 'عائد'),
    ('envoy', 'موفد'),
    ('returning demonstrator', 'معيد عائد'),
    ('loathes', 'مستنكف'),
    ('transfer outside the university', 'نقل خارج الجامعة'),
    ('end services', 'انهاء خدمات'),
    ('resigned', 'انهاء بحكم المستقيل'),
]

NOMINATION_REASON_CHOICES = [
    ('contest', 'مسابقة'),
    ('First graduate', 'خريج أول')
]


YEAR_VALIDATOR = RegexValidator(
    r'^[0-9]{4}[-][0-9]{4}$', 'أدخل السنة الجامعية بتنسيق: YYYY-YYYY مثل 2022-2023'
)


DECISION_TYPE_CHOICES = [
    ('s', 'ش.ع'),
    ('o', 'و'),
    ('b', 'ب'),
]


EXCELLENCE_YEAR_CHOICES = [
    ('1', 'سنة أولى'),
    ('2', 'سنة ثانية'),
    ('3', 'سنة ثالثة'),
    ('4', 'سنة رابعة'),
    ('5', 'سنة خامسة'),
    ('6', 'سنة سادسة'),
    ('g', 'تخرج')
]

EXCELLENCE_DEGREE_CHOICES = [
    ('1', 'الأول'),
    ('2', 'الثاني'),
    ('3', 'الثالث')
]


GRADUATE_STUDIES_DEGREE_CHOICES = [
    ('diploma', 'دبلوم'),
    ('master', 'ماجستير'),
    ('ph.d', 'دكتوراه'),
]


CERTIFICATE_TYPE = [
    ('language', 'لغة'),
    ('master', 'ماجستير'),
    ('ph.d', 'دكتوراه'),
]

DISPATCH_TYPE = [
    ('inner', 'داخلي'),
    ('outer', 'خارجي'),
]

ALIMONY = [
    ('grant', 'منحة'),
    ('seat', 'مقعد'),
]
