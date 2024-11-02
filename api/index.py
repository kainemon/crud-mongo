from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve MongoDB connection details from environment variables
mongodb_uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# Establish a connection to the MongoDB database
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Root endpoint
@app.route("/", methods=["GET"])
def index():
    return jsonify({ "message": "Up & Running..." })

# Endpoint to create a new book entry
@app.route("/book", methods=["POST"])
def create_book():
    data = request.json  # Get JSON data from the request
    result = collection.insert_one(data)  # Insert the new book into the collection
    return jsonify({"message": "Book created successfully!", "id": str(result.inserted_id)}), 201

# Endpoint to retrieve all books
@app.route("/books", methods=["GET"])
def get_books():
    books = list(collection.find())  # Fetch all book documents from the collection
    for book in books:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSON serialization
    return jsonify(books)

# Endpoint to retrieve a specific book by ID
@app.route("/book/<id>", methods=["GET"])
def get_book(id):
    book = collection.find_one({"_id": ObjectId(id)})  # Find the book by its ObjectId
    if book:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string
        return jsonify(book)
    return jsonify({"error": "Book not found!"}), 404  # Return error if not found

# Endpoint to update an existing book by ID
@app.route("/book/<id>", methods=["PUT"])
def update_book(id):
    data = request.json  # Get JSON data from the request
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})  # Update the book
    if result.modified_count:
        return jsonify({"message": "Book updated successfully!"})
    return jsonify({"error": "Book not found!"}), 404  # Return error if not found

# Endpoint to delete a book by ID
@app.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    result = collection.delete_one({"_id": ObjectId(id)})  # Delete the book from the collection
    if result.deleted_count:
        return jsonify({"message": "Book deleted successfully!"})
    return jsonify({"error": "Book not found!"}), 404  # Return error if not found