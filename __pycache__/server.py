from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.asgi import GraphQL
from resolvers import query

#GRAPH QL

type_defs = load_schema_from_path("C:\\Users\\diego\\Desktop\\Trabajo\\test\\trabalho")
schema = make_executable_schema(type_defs, query)

#APP
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)