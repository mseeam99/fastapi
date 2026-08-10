from fastapi import FastAPI, Body
import json

app = FastAPI()

@app.get("/")
async def startingPage():
    return "Starting Main Page !"

@app.get("/books")
async def allBooks():
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/books/id/{bookId}")
async def returnByBookId(bookId):
    #find book by book id
    bookId = int(bookId)
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    bookList = data["books"]
    returnByBookId = None
    for i in range(len(bookList)):
        if bookList[i]["book_id"] == bookId:
            returnByBookId = bookList[i]
            break
    if returnByBookId == None:
        return "BOOK ID DOES NOT EXIST"
    return returnByBookId

@app.get("/books/authorName/{authorName}")
async def returnByBookId(authorName: str):
    authorName = str(authorName)
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    booksList = data["books"]
    listOfBookObjectByAuthorName = []
    for i in range(len(booksList)):
        authorObjectAsList = booksList[i]["authors"]
        for j in range(len(authorObjectAsList)):
            authorObject = authorObjectAsList[j]
            if authorObject["name"] == authorName:
                listOfBookObjectByAuthorName.append(booksList[i])
    if len(listOfBookObjectByAuthorName) == 0:
        return "NO BOOK UNDER THIS AUTHOR EXISTS"
    return listOfBookObjectByAuthorName
    
@app.get("/books/authorNameAndPublishedYear/{authorName}/{publishedYear}")
async def returnByBookId(authorName: str, publishedYear: int):
    authorName = str(authorName)
    publishedYear = int(publishedYear)
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    booksList = data["books"]
    listOfBookObjectByAuthorNameAndYear = []
    sameAuthor = False
    publishYear = False
    for i in range(len(booksList)):
        authorObjectAsList = booksList[i]["authors"]
        for j in range(len(authorObjectAsList)):
            authorObject = authorObjectAsList[j]
            if authorObject["name"] == authorName:
                sameAuthor = True
        metaDataObject = booksList[i]["metadata"]
        publishedYearObject = metaDataObject["published"]
        year = publishedYearObject["year"]
        if year == publishedYear:
            publishYear = True
        if sameAuthor == True and publishYear == True:
            listOfBookObjectByAuthorNameAndYear.append(booksList[i])
        sameAuthor = False
        publishYear = False
    if len(listOfBookObjectByAuthorNameAndYear) == 0:
        return "NO BOOK UNDER THIS AUTHOR AND PUBLISHED DATE EXISTS"
    return listOfBookObjectByAuthorNameAndYear

    ### Query Param
    @app.get("/books/authorName/")
    async def returnByBookId(authorName: str, publishedYear: int):
        data = None
        with open("books.json", "r") as file:
            data = json.load(file)    
        booksList = data["books"]
        listOfBookObjectByAuthorNameAndYear = []
        for i in range(len(booksList)):
            sameAuthor = False
            publishYear = False
            authorObjectAsList = booksList[i]["authors"]
            for j in range(len(authorObjectAsList)):
                authorObject = authorObjectAsList[j]
                if authorObject["name"] == authorName:
                    sameAuthor = True
                    break
            metaDataObject = booksList[i]["metadata"]
            publishedYearObject = metaDataObject["published"]
            year = publishedYearObject["year"]
            if year == publishedYear:
                publishYear = True
            if sameAuthor == True and publishYear == True:
                listOfBookObjectByAuthorNameAndYear.append(booksList[i])
        if len(listOfBookObjectByAuthorNameAndYear) == 0:
            return "NO BOOK UNDER THIS AUTHOR AND PUBLISHED DATE EXISTS"
        return listOfBookObjectByAuthorNameAndYear
    ###

@app.post("/books/createbook")
async def createBook(newBook: dict = Body(...)):
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    data["books"].append(newBook)
    with open("books.json", "w") as file:
        json.dump(data, file, indent=2)
    return 200

@app.put("/books/updateEntire")
async def updateEntire(newLibraryObject: dict = Body(...)):
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    data = newLibraryObject
    with open("books.json", "w") as file:
        json.dump(data, file, indent=2)
    return 200

@app.patch("/books/updatePartialLibrary")
async def updatePartialLibrary(newLibraryObject: dict = Body(...)):
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    data["library"].update(newLibraryObject)
    with open("books.json", "w") as file:
        json.dump(data, file, indent=2)
    return 200

@app.delete("/books/deleteBook/{id}")
async def deleteBook(bookId:int):
    data = None
    with open("books.json", "r") as file:
        data = json.load(file)
    bookList = data["books"]
    found = False
    for i in range(len(bookList)):
        bookObj = bookList[i]
        if bookObj["book_id"] == bookId:
            bookList.pop(i)
            found = True
            break
    if found == False:
        return "Book Does not exist"
    data["books"] = bookList
    with open("books.json", "w") as file:
        json.dump(data, file, indent=2)
    return 200