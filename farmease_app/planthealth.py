from kindwise import PlantApi

api = PlantApi('3srgfK8yEjIu5GZkZIStHHe8wqwgC71zpV7IAhdwDQjuZLK0B8')
identification = api.health_assessment(r'C:\Users\User\farmease\FARMEASE\media\plant.jpeg', details=['description', 'treatment'])


print('is healthy' if identification.result.is_healthy.binary else 'has disease')
for suggestion in identification.result.disease.suggestions:
    print(suggestion.name)
    print(f'probability {suggestion.probability:.2%}')
    print(suggestion.details['description'])
    print(suggestion.details['treatment'])
    print()