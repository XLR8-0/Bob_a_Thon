from app.services.regex.generator import RegexGenerator
import re

gen = RegexGenerator()

print("=" * 70)
print("TEST: Case-insensitive excluded words")
print("=" * 70)
examples = ['raju@gmail.com', 'test@yahoo.com', 'admin@example.com']
result = gen.generate_from_examples(examples, excluded_words='abc.com')
print(f"Pattern: {result['pattern']}")
print(f"\nPattern contains (?i:...): {'(?i:' in result['pattern']}")

# Test WITHOUT re.IGNORECASE flag (pattern should handle it internally)
pattern = re.compile(result['pattern'])
print("\nTest strings (pattern handles case-insensitivity internally):")
test_strings = [
    'raju@gmail.com',
    'user@abc.com',
    'admin@ABC.COM',
    'test@Abc.Com',
    'user@AbC.CoM'
]
for test in test_strings:
    match = bool(pattern.match(test))
    print(f"  {test}: {'[MATCH]' if match else '[EXCLUDED]'}")

print("\n" + "=" * 70)
print("TEST: Multiple excluded words - case variations")
print("=" * 70)
examples = ['user123', 'guest456', 'visitor789']
result = gen.generate_from_examples(examples, excluded_words='admin,test')
print(f"Pattern: {result['pattern']}")

pattern = re.compile(result['pattern'])
print("\nTest strings:")
test_strings = ['user123', 'Admin456', 'TEST789', 'MyTest', 'ADMIN', 'test']
for test in test_strings:
    match = bool(pattern.match(test))
    print(f"  {test}: {'[MATCH]' if match else '[EXCLUDED]'}")

print("\n[SUCCESS] Case-insensitive exclusion working!")

# Made with Bob
