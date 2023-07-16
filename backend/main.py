from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(DevConfig)

CORS(app)
CORS(app, origins=['http://127.0.0.1:5500'])


db.init_app(app)

migrate = Migrate(app, db)

api = Api(app, doc='/docs')

# model (serializer)
recipe_model = api.model(
    "Recipe",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "description": fields.String()
    }
)

@api.route('/hello')
class helloResource(Resource):
    def get(self):
        return {"message": "hello world"}


     
    
@api.route('/recipes')
class RecipesResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self):
        """Get all Recipes """
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
    def post(self):
        """Create a new recipe"""
        
        data = request.get_json()
        
        new_recipe = Recipe(
            title=data.get('title'),
            description=data.get('description')
        )
        new_recipe.save()
        
        return new_recipe, 201

@api.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self, id):
        """Get a recipe by id"""
        recipe = Recipe.query.get_or_404(id)
        return recipe

    @api.marshal_with(recipe_model)
    def put(self, id):
        """Update a recipe by id"""
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'), data.get('description'))
        return recipe_to_update

    @api.marshal_with(recipe_model)
    def delete(self, id):
        """Delete a recipe by id"""
        recipe_to_delete = Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Recipe": Recipe
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
