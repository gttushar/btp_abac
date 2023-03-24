from owlready2 import *
import owlready2, rdflib

# abac = get_ontology("http://www.semanticweb.org/tushar/ontologies/2021/abac#").load()
abac = get_ontology("file://C:\\Users\\Tushar\\Desktop\\btp_abac_heirarchy\\abac.owl").load()

class SparqlQueries:
	def __init__(self):
		# owlready2.JAVA_EXE = "C:\\Program Files\\Java\\jre1.8.0_321\\bin\\java.exe"
		my_world = World()
		my_world.get_ontology("file://C:\\Users\\Tushar\\Desktop\\btp_abac_heirarchy\\abac.owl").load() #path to the owl file is given here
		# sync_reasoner(my_world)  #reasoner is started and synchronized here
		self.graph = my_world.as_rdflib_graph()

	def search(self, query, distance = -1):
		#Base URL of your ontology has to be given here
		query = """ base <http://www.semanticweb.org/tushar/ontologies/2021/abac> 
					prefix xsd: <http://www.w3.org/2001/XMLSchema#> """ + query
		#query is being run
		resultsList = self.graph.query(query) #, initBindings={'node': node })
		#creating json object
		response = []
		for item in resultsList:
			# s = str(item['s'].toPython())
			# s = re.sub(r'.*#',"",s)
			# response.append(s)

			o = None
			if distance == -1:
				o = str(item['o'].toPython())
			else:
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
		for distance in range(max_distance + 1):
			select = '?s '
			where = ''
			optional = ''
			predicate = '(owl:equivalentClass|^owl:equivalentClass)*/(rdfs:subClassOf|^rdfs:subClassOf|rdf:type|^rdf:type)/(owl:equivalentClass|^owl:equivalentClass)*'
			# predicate = '(rdfs:subClassOf|^rdfs:subClassOf|rdf:type|^rdf:type)'
			# using UNION since logical OR is not supported
			if distance > 0:
				select += '?o' + str(distance)
				# where = '?s ?p1 ?o1 .\n'
				where = '{ ?s ' + predicate + ' ?o1 } ' + \
						' .\n'
						# 'UNION { ?s owl:equivalentClass|^owl:equivalentClass ?mid1 . ?mid1 ?p1 ?o1 }' + \
						# 'UNION { ?o1 rdfs:subClassOf ?s }' + \
				# optional = '?o1 ?p1 ?s .\n'
				for i in range(2, distance + 1):
					# where += '?o' + str(i - 1) + ' ?p' + str(i) + ' ?o' + str(i) + ' .\n'
					where += '{ ?o' + str(i - 1) + ' ' + predicate + ' ?o' + str(i) + '}' + \
							 ' .\n'
							 # 'UNION { ?o' + str(i - 1) + ' owl:equivalentClass|^owl:equivalentClass ?mid' + str(i) + \
							 		# ' . ?mid' + str(i) + ' ?p' + str(i) + ' ?o' + str(i) + ' }' + \
					# optional += '?o' + str(i) + ' rdfs:subClassOf ?o' + str(i - 1) + ' .\n'

			query = 'SELECT ' + select + '\nWHERE {\n' + where \
				  + 'FILTER (?s = <http://www.semanticweb.org/tushar/ontologies/2021/abac#' + element + '>' + \
				    ') \n' \
				  + '}'
			for i in range(1, distance + 1):
				for ignored in ['Class', 'NamedIndividual']:
					query = query[0 : -4] + ' && ?o' + str(i) + ' != owl:' + ignored + query[-4 : ]
					# + 'OPTIONAL {\n' + optional + '} \n' \
			# print('query = \n' + query)
			for item in self.search(query, distance):
				result.add(item)

		# print('element = ' + element); print('result =');print(result);
		return list(result)

	def distance_search2(self, element, max_distance):
		if max_distance == 0: return [element]

		# result = [set() for i in range(max_distance)]
		# result[0] = set([element])
		visited = set([element])
		leaves = set([element])

		for distance in range(1, max_distance + 1):
			temp = set()
			predicate = '(owl:equivalentClass|^owl:equivalentClass)*/(rdfs:subClassOf|^rdfs:subClassOf|rdf:type|^rdf:type)/(owl:equivalentClass|^owl:equivalentClass)*'
			elements = ''.join(['(<http://www.semanticweb.org/tushar/ontologies/2021/abac#'+element+'>) ' for element in leaves])

			# query = 'SELECT ?o WHERE { ?s ' + predicate + ' ?o. FILTER (?s IN (' + elements + ' ) \n}'
			query = 'SELECT ?o WHERE { VALUES (?s) {'+elements+'}\n ?s ' + predicate + ' ?o. FILTER (?o != owl:Class && ?o != owl:NamedIndividual) \n}'
			# ignore_list = ['Class', 'NamedIndividual']
			# query = query[0 : -4] + '?o != owl:' + ignore_list[0] + query[-4 : ]
			# for ignored in ignore_list[1:]:
			# 	query = query[0 : -4] + ' && ?o != owl:' + ignored + query[-4 : ]

			# print('query = \n' + query)
			# temp.update( self.search(query, -1) )
			leaves = set( self.search(query, -1) ) - visited
			if not leaves:
				break
			visited.update(leaves)
			# result[distance] = temp - result[distance - 1]

		# print('element = ' + element); print('result =');print(visited);
		return list(visited)


	def ancestor_search(self, element):
		result = set()
		# runQuery = SparqlQueries()
		# max_distance = 5
		# node = 'Professor'
		select = '?s '
		where = ''
		optional = ''
		select += '?o'
		where = '?s (rdfs:subClassOf|rdf:type)* ?o .\n'
		# where = '{ ?s ?p ?o } UNION { ?o rdfs:subClassOf ?s } .\n'
		# optional = '?o1 ?p1 ?s .\n'

		query = 'SELECT ' + select + '\nWHERE {\n' + where \
				+ 'FILTER (?s = <http://www.semanticweb.org/tushar/ontologies/2021/abac' + '#' + element + '>) \n' \
				+ '}'
				# + 'OPTIONAL {\n' + optional + '} \n' \
		# print('query = ' + query)
		for item in self.search(query):
			result.add(item)

		# print('element = ' + element); print('ancestors =');print(result);
		return list(result)

	def descendant_search(self, element):
		result = set()
		# runQuery = SparqlQueries()
		# max_distance = 5
		# node = 'Professor'
		select = '?s '
		where = ''
		optional = ''
		select += '?o'
		where = '?o (rdfs:subClassOf|rdf:type)* ?s .\n'
		# where = '{ ?s ?p ?o } UNION { ?o rdfs:subClassOf ?s } .\n'
		# optional = '?o1 ?p1 ?s .\n'

		query = 'SELECT ' + select + '\nWHERE {\n' + where \
				+ 'FILTER (?s = <http://www.semanticweb.org/tushar/ontologies/2021/abac' + '#' + element + '>) \n' \
				+ '}'
				# + 'OPTIONAL {\n' + optional + '} \n' \
		# print('query = ' + query)
		for item in self.search(query):
			result.add(item)

		# print('element = ' + element); print('descendants =');print(result);
		return list(result)

# runQuery = SparqlQueries()
# print(runQuery.distance_search('Course', 3))

# query = """ SELECT ?s ?p ?o ?p1 ?oo
# 			WHERE {
# 			    ?s ?p ?o .
# 			    FILTER (str(?s) = <http://www.semanticweb.org/tushar/ontologies/2021/abac""" + '#' + node + """>)
# 				OPTIONAL { ?o ?p1 ?oo . }
# 			} """