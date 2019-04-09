from token import *
from ast import *
import scanner

def try_consume(scanner, token_type):
	if scanner.peek().type == token_type:
		return scanner.next()
	else:
		return None

def parse_expression(scanner):
	return parse_tuple_expression(scanner)

def parse_tuple_expression(scanner):
	tuple_elements = [parse_addition_expression(scanner)]
	while try_consume(scanner, TokenType.OP_COMMA):
		tuple_elements += [parse_addition_expression(scanner)]
	if len(tuple_elements) == 1:
		return tuple_elements[0]
	else:
		return TupleExpression(tuple_elements)

def parse_addition_expression(scanner):
	left = parse_multiplication_expression(scanner)
	if not left:
		return None
	while scanner.peek().type in (TokenType.OP_PLUS, TokenType.OP_MINUS):
		if scanner.next().type == TokenType.OP_PLUS:
			Node = AddExpression
		else:
			Node = SubtractExpression
		right = parse_multiplication_expression(scanner)
		left = Node(left, right)
	return left

def parse_multiplication_expression(scanner):
	left = parse_parenthesized_expression(scanner)
	if not left:
		return None
	while scanner.peek().type in (TokenType.OP_MULT, TokenType.OP_DIV):
		if scanner.next().type == TokenType.OP_MULT:
			Node = MultiplyExpression
		else:
			Node = DivideExpression
		right = parse_parenthesized_expression(scanner)
		left = Node(left, right)
	return left

def parse_parenthesized_expression(scanner):
	open_parenthesis = try_consume(scanner, TokenType.LPAR)
	if open_parenthesis:
		internal_expression = parse_expression(scanner)
		if not try_consume(scanner, TokenType.RPAR):
			print("Error: Missing ')' to close '('.")
			print(open_parenthesis)
		return internal_expression
	else:
		return parse_id_expression(scanner)

def parse_id_expression(scanner):
	id_token = try_consume(scanner, TokenType.ID)
	if id_token:
		if try_consume(scanner, TokenType.OP_DOT):
			integer_literal = try_consume(scanner, TokenType.INT_LIT)
			if not integer_literal:
				print("Error: Index of tuple must be an integer literal.")
			return TupleAccessExpression(id_token, integer_literal)
		elif try_consume(scanner, TokenType.LBRAK):
			index_expression = parse_expression(scanner)
			if not try_consume(scanner, TokenType.RBRAK):
				print("Error: Missing ']' to close '['.")
			return ArrayAccessExpression(id_token, index_expression)
		else:
			argument_expression = parse_id_expression(scanner)
			if argument_expression:
				return FunctionCallExpression(id_token, argument_expression)
			else:
				return IdentifierExpression(id_token)
	elif scanner.peek().type == TokenType.INT_LIT:
		return IntegerLiteralExpression(scanner.next())
	else:
		print("Error: invalid expression.")

s = scanner.Scanner(string="sq a + sq b")
p = parse_expression(s)
print(p)		
		