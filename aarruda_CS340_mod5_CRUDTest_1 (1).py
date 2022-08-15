from aarruda_CS340_mod5_CRUD import AnimalShelter

# Create and Read test script

# Assign test data to variables

testDocs = [{
        "_id" : "ObjectId(629000cd2866fd3280524161)",
        "1" : 4,
        "age_upon_outcome" : "7 months",
        "animal_id" : "A733653",
        "animal_type" : "Cat",
        "breed" : "Siamese Mix",
        "color" : "Seal Point",
        "date_of_birth" : "2016-01-25",
        "datetime" : "2016-08-27 18:11:00",
        "monthyear" : "2016-08-27T18:11:00",
        "name" : "Kitty",
        "outcome_subtype" : "",
        "outcome_type" : "Adoption",
        "sex_upon_outcome" : "Intact Female",
        "location_lat" : 30.3188063374257,
        "location_long" : -97.7240376703891,
        "age_upon_outcome_in_weeks" : 30.8225198412698
    },

    {
        "_id": "ObjectId(629000cd2866fd3280524162)",
        "1" : 8,
        "age_upon_outcome" : "1 year",
        "animal_id" : "A736551",
        "animal_type" : "Dog",
        "breed" : "Labrador Retriever/Australian Cattle Dog",
        "color" : "Black",
        "date_of_birth" : "2015-10-12",
        "datetime" : "2016-11-27 18:00:00",
        "monthyear" : "2016-11-27T18:00:00",
        "name" : "*Mia",
        "outcome_subtype" : "",
        "outcome_type" : "Adoption",
        "sex_upon_outcome" : "Spayed Female",
        "location_lat" : 30.4443212820182,
        "location_long" : -97.7326980338793,
        "age_upon_outcome_in_weeks" : 58.9642857142857
    },
    
    {
        "_id" : "ObjectId(629000cd2866fd328052416c)",
        "1" : 5,
        "age_upon_outcome" : "2 years",
        "animal_id" : "A691584",
        "animal_type" : "Dog",
        "breed" : "Labrador Retriever Mix",
        "color" : "Tan/White",
        "date_of_birth" : "2012-11-06",
        "datetime" : "2015-05-30 13:48:00",
        "monthyear" : "2015-05-30T13:48:00",
        "name" : "Luke",
        "outcome_subtype" : "",
        "outcome_type" : "Return to Owner",
        "sex_upon_outcome" : "Neutered Male",
        "location_lat" : 30.7104815618433,
        "location_long" : -97.562297435286,
        "age_upon_outcome_in_weeks" : 133.653571428571
    }]

AnimalShelter.__init__(AnimalShelter, "aacuser", "1qaz!QAZ")

def testCreate():
    shelter = AnimalShelter(username, password)
    data = testDocs[0]
    
    if shelter.create(data):
        print("Animal Added")

def testRead():
    shelter = AnimalShelter(username, password)
    dogsAdopted = shelter.read({"animal_type" : "Dog", "outcome_type" : "Adoption"})
    for adoptedDogs in dogsAdopted:
        print (adoptedDogs)
        
def testUpdate():
    shelter = AnimalShelter(username, password)
    query = {name: "*Mia"}
    update = {'$set': {name: "Mia"}}
    
    updateDoc = shelter.update_one(query, update)
    for docs in testDocs.find({'name': "Mia"}):
        print(docs)
    
def testDelete():
    shelter = AnimalShelter(username, password)
    
    docDeleted = shelter.delete_many({"sex_upon_outcome" : "Intact Female"})
    for docs in testDocs.find({"sex_upon_outcome" : "Intact Female"}):
        print(docs)
    


test1 = testCreate()
test2 = testRead()
test3 = testUpdate()
test4 = testDelete()

print (test1)
print (test2)
print (test3)
print (test4)