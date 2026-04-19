{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "f2ff41e1",
   "metadata": {},
   "outputs": [],
   "source": [
    "from pymongo import MongoClient\n",
    "from bson.objectid import ObjectId\n",
    "\n",
    "class AnimalShelter:\n",
    "    \"\"\"\n",
    "    CRUD operations for the Animal collection in MongoDB.\n",
    "    \"\"\"\n",
    "\n",
    "    def __init__(self, user='aacuser', password='AACpass123', host='nv-desktop-services.apporto.com', port=32409, db='AAC', col='animals'):\n",
    "        \"\"\"\n",
    "        Initialize the connection to the MongoDB database and collection.\n",
    "        \"\"\"\n",
    "        try:\n",
    "            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')\n",
    "            self.database = self.client[db]\n",
    "            self.collection = self.database[col]\n",
    "        except Exception as e:\n",
    "            print(f\"Error connecting to MongoDB: {e}\")\n",
    "\n",
    "    def create(self, data):\n",
    "        \"\"\"\n",
    "        Insert a document into the collection.\n",
    "        \n",
    "        Parameters:\n",
    "        data (dict): The document to insert into MongoDB\n",
    "        \n",
    "        Returns:\n",
    "        bool: True if successful, False otherwise\n",
    "        \"\"\"\n",
    "        if data:\n",
    "            try:\n",
    "                self.collection.insert_one(data)\n",
    "                return True\n",
    "            except Exception as e:\n",
    "                print(f\"Insert failed: {e}\")\n",
    "                return False\n",
    "        else:\n",
    "            raise ValueError(\"Nothing to save, because data parameter is empty\")\n",
    "\n",
    "    def read(self, query):\n",
    "        \"\"\"\n",
    "        Query for documents from the collection using find().\n",
    "        \n",
    "        Parameters:\n",
    "        query (dict): Key/value pair to filter documents\n",
    "        \n",
    "        Returns:\n",
    "        list: A list of documents if found, otherwise an empty list\n",
    "        \"\"\"\n",
    "        try:\n",
    "            if not isinstance(query, dict):\n",
    "                raise ValueError(\"Query must be a dictionary\")\n",
    "            cursor = self.collection.find(query)\n",
    "            return list(cursor)\n",
    "        except Exception as e:\n",
    "            print(f\"Query failed: {e}\")\n",
    "            return []\n",
    "\n",
    "    def update(self, query, new_values):\n",
    "        \"\"\"\n",
    "        Update documents in the collection.\n",
    "        \n",
    "        Parameters:\n",
    "        query (dict): Filter for documents to update\n",
    "        new_values (dict): New values to apply\n",
    "        \n",
    "        Returns:\n",
    "        int: Number of modified documents\n",
    "        \"\"\"\n",
    "        if query and new_values:\n",
    "            try:\n",
    "                result = self.collection.update_many(query, {\"$set\": new_values})\n",
    "                return result.modified_count\n",
    "            except Exception as e:\n",
    "                print(f\"Update failed: {e}\")\n",
    "                return 0\n",
    "        else:\n",
    "            raise ValueError(\"Query or new values missing\")\n",
    "\n",
    "    def delete(self, query):\n",
    "        \"\"\"\n",
    "        Delete documents from the collection.\n",
    "        \n",
    "        Parameters:\n",
    "        query (dict): Filter for documents to delete\n",
    "        \n",
    "        Returns:\n",
    "        int: Number of deleted documents\n",
    "        \"\"\"\n",
    "        if query:\n",
    "            try:\n",
    "                result = self.collection.delete_many(query)\n",
    "                return result.deleted_count\n",
    "            except Exception as e:\n",
    "                print(f\"Delete failed: {e}\")\n",
    "                return 0\n",
    "        else:\n",
    "            raise ValueError(\"Query missing\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d844ca03",
   "metadata": {},
   "outputs": [],
   "source": [
    "from aac_crud_module import AnimalShelter\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "408ce3cf",
   "metadata": {},
   "outputs": [],
   "source": [
    "shelter = AnimalShelter()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "6bdb9bc9",
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_data = {\n",
    "    \"name\": \"TestDog\",\n",
    "    \"breed\": \"TestBreed\",\n",
    "    \"animal_type\": \"Dog\",\n",
    "    \"age_upon_outcome\": \"1 year\",\n",
    "    \"outcome_type\": \"Adoption\"\n",
    "}\n",
    "\n",
    "shelter.create(sample_data)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "f921c6f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "results = shelter.read({\"name\": \"TestDog\"})\n",
    "for doc in results:\n",
    "    print(doc)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b1update1",
   "metadata": {},
   "outputs": [],
   "source": [
    "updated_count = shelter.update({\"name\": \"TestDog\"}, {\"breed\": \"UpdatedBreed\"})\n",
    "print(\"Documents updated:\", updated_count)\n",
    "\n",
    "results = shelter.read({\"name\": \"TestDog\"})\n",
    "for doc in results:\n",
    "    print(doc)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b1delete1",
   "metadata": {},
   "outputs": [],
   "source": [
    "deleted_count = shelter.delete({\"name\": \"TestDog\"})\n",
    "print(\"Documents deleted:\", deleted_count)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a5b68bd9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}