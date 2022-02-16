from owlready2 import *
import owlready2, rdflib

# abac = get_ontology("http://www.semanticweb.org/tushar/ontologies/2021/abac#").load()
abac = get_ontology("file://C:\\Users\\Tushar\\Desktop\\btp_flask\\abac.owl").load()

class SparqlQueries:
	def __init__(self):
		# owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_321\\bin\\java.exe"
		my_world = World()
		my_world.get_ontology("file://C:\\Users\\Tushar\\Desktop\\btp_flask\\abac.owl").load() #path to the owl file is given here
		# sync_reasoner(my_world)  #reasoner is started and synchronized here
		self.graph = my_world.as_rdflib_graph()

	def search(self, query, distance):
		#Base URL of your ontology has to be given here
		query = """ base <http://www.semanticweb.org/tushar/ontologies/2021/abac> 
					prefix xsd: <http://www.w3.org/2001/XMLSchema#> """ + query
		#query is being run
		resultsList = self.graph.query(query) #, initBindings={'node': node })
		#creating json object
		response = []
		for item in resultsList:
			s = str(item['s'].toPython())
			s = re.sub(r'.*#',"",s)
			response.append(s)

			o = str(item['o' + str(distance)].toPython())
			o = re.sub(r'.*#', "", o)
			response.append(o)
			# response.append({'s' : s, 'p' : p, "o" : o})

		# print(response) #just to show the output
		return response

	def distance_search(self, element, max_distance):
		if max_distance == 0:
			return [element]

		result = set()
		# runQuery = SparqlQueries()
		# max_distance = 5
		# node = 'Professor'
		for distance in range(max_distance + 1):
			select = '?s '
			where = ''
			optional = ''
			if distance > 0:
				select += '?o' + str(distance)
				# where = '?s ?p1 ?o1 .\n'
				where = '{ ?s ?p1 ?o1 } UNION { ?o1 rdfs:subClassOf ?s } .\n'
				# optional = '?o1 ?p1 ?s .\n'
				for i in range(2, distance + 1):
					# where += '?o' + str(i - 1) + ' ?p' + str(i) + ' ?o' + str(i) + ' .\n'
					where += '{ ?o' + str(i - 1) + ' ?p' + str(i) + ' ?o' + str(i) + '} UNION ' \
							 + '{ ?o' + str(i) + ' rdfs:subClassOf ?o' + str(i - 1) + '}' + ' .\n'
					# optional += '?o' + str(i) + ' rdfs:subClassOf ?o' + str(i - 1) + ' .\n'

			query = 'SELECT ' + select + '\nWHERE {\n' + where \
					+ 'FILTER (?s = <http://www.semanticweb.org/tushar/ontologies/2021/abac' + '#' + element + '>) \n' \
					+ '}'
					# + 'OPTIONAL {\n' + optional + '} \n' \
			# print('query = ' + query)
			for item in self.search(query, distance):
				result.add(item)

		# print('element = ' + element); print('result =');print(result);
		return list(result)

# runQuery = SparqlQueries()
# print(runQuery.distance_search('Course', 3))

	# query = """ SELECT ?s ?p ?o ?p1 ?oo
	# 			WHERE {
	# 			    ?s ?p ?o .
	# 			    FILTER (str(?s) = <http://www.semanticweb.org/tushar/ontologies/2021/abac""" + '#' + node + """>)
	# 				OPTIONAL { ?o ?p1 ?oo . }
	# 			} """