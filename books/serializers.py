from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(child=serializers.CharField(), write_only=True) # Accept a list of author names, where each author name is a string from the user for writing.
    
    # SerializerMethodField is a special field in Django REST Framework (DRF) used to compute values dynamically by calling a method on the serializer class.
    # author_names = serializers.SerializerMethodField(read_only=True) # For reading, return the nested details of the authors.
        
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors',          # Accepts list of author names for writing
            #'author_names',   # Provides detailed author info when reading
            'isbn',
            'publication_date',
            'publisher',
            'genres',
            'summary',
            'number_of_pages',
            'language',
            'price',
            'stock',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        author_names = validated_data.pop('authors', [])
     
        book = Book.objects.create(**validated_data)
        author_objs = []
        for name in author_names:
            name = name.strip()
            if name:
                author_obj, created = Author.objects.get_or_create(name=name)
                author_objs.append(author_obj)
                
        book.authors.set(author_objs)
        return book

    def update(self, instance, validated_data):
        author_names = validated_data.pop('authors', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if author_names is not None:
            author_objs = []
            for name in author_names:
                name = name.strip()
                if name:
                    author_obj, created = Author.objects.get_or_create(name=name)
                    author_objs.append(author_obj)
            instance.authors.set(author_objs)
        return instance
    
    def validate_isbn(self, value):
        """
        Validate that the ISBN is either 10 or 13 characters long.
        """
        isbn_digits = value.replace('-', '') # Remove hyphens if any, to check only the digits
        
        # Check length (allowing only ISBN-10 or ISBN-13)
        if len(isbn_digits) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be either 10 or 13 characters long.")
        
        # Optional: Check if all characters are digits
        if not isbn_digits.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits (or hyphens as separators).")
        
        return value
    
    '''
    # DRF automatically looks for a method named get_<field_name>. So, for author_details, DRF will call get_author_details
    # field_name should be one of field names defined in the model else a new field with the given field name will get displayed/ returned during get request
    # use serializers.SerializerMethodField to create a field for displaying through this custom function
    def get_authors(self, obj): # Here, obj refers to the current Book instance
        # Use your existing AuthorSerializer to return author details.
        return [{'name': author.name, 'bio':author.bio} for author in obj.authors.all()]    
    '''

    # Alternative to the above get_authors(self, obj): function
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['authors'] = [{'name': author.name, 'bio': author.bio} for author in instance.authors.all()]
        return rep

'''
There are two common approaches when dealing with ManyToMany relationships:
1. Using Primary Keys: This approach lets clients submit IDs for authors and genres.
2. Using Nested Serialization: This shows detailed information when reading, though writing nested objects requires extra work.
'''
'''
    # Use PrimaryKeyRelatedField for writable relationships
    #authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    #genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    #authors = AuthorSerializer(many=True, read_only=True) # Serializes all related authors using the AuthorSerializer in a nested, detailed view.
    #genres = GenreSerializer(many=True, read_only=True) # Similar to authors, it serializes all related genres in detail for output, without accepting input for writes.
    #author_ids = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, write_only=True)
    #genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, write_only=True)


'''