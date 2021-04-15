# Todo.txt I/O

A simple Python module to parse, manipulate and write [Todo.txt](http://todotxt.com/) data.

This module tries to comply to the [Todo.txt specifications](https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format) (disclaimer: there aren't any unit tests).

It is a quite heavily modified version of [this](https://epocdotfr.github.io/todotxtio/).
The documentation for the Todo class is still pretty accurate.  But I have added a TodoList class as well as some extra functions.

## Documentation

### Simple usage (quickstart):
```
from todotxtio import TodoList, Todo
todolist = TodoList()

# Create and show a simple todo-entry

todo = Todo(text="Ask for help", projects=['Todotxtio'])
todo.contexts.append('Home')

print(todo.to_dict())
# {'text': 'Ask for help', 'completed': False, 'completion_date': None, 'priority': None, 'creation_date': None, 'projects': ['Todotxtio'], 'contexts': ['Home'], 'tags': {}}


# Add some entries to the list

todolist.append(todo)

todo = Todo(text="Buy groceries", projects=['Shopping', 'Dinner'], contexts=['Away'])
todolist.append(todo)

todo = Todo(text="Drive to work", projects=['Work'], contexts=['Away'])
todolist.append(todo)

todo = Todo(text="Complete README", projects=['Todotxtio'], contexts=['Home'])
todolist.append(todo)



print(todolist)
[(0, Ask for help +Todotxtio @Home), (1, Buy groceries +Shopping +Dinner @Away), (2, Drive to work +Work @Away), (3, Complete README +Todotxtio @Home)]


# You can also add some magic functions to the lists
print(todolist.sorted)
[(0, Ask for help +Todotxtio @Home), (1, Buy groceries +Shopping +Dinner @Away), (2, Complete README +Todotxtio @Home), (3, Drive to work +Work @Away)]


print(todolist.to_markdown())
# - [ ] Ask for help
# - [ ] Complete README
# - [ ] Buy groceries
# - [ ] Drive to work


# And also some inline search and filtering:

print(todolist.contexts(['Home', 'Away']).incomplete.sorted.to_markdown(projects=True))
# - [ ] Ask for help (Todotxtio)
# - [ ] Buy groceries (Shopping, Dinner)
# - [ ] Complete README (Todotxtio)
# - [ ] Complete README (Todotxtio)
# - [ ] Drive to work (Work)

# Change an entry in the todolist:

searchresult = todolist.search(exact="Drive to work")
index, todo = searchresult[0]
todo.completed = True
todolist.replace(todo, index)

print(todolist.contexts(['Home', 'Away']).sorted.to_markdown(projects=True))
# - [ ] Ask for help (Todotxtio)
# - [ ] Buy groceries (Shopping, Dinner)
# - [ ] Complete README (Todotxtio)
# - [x] Drive to work (Work)


print(todolist.contexts(['Home', 'Away']).completed.to_markdown(contexts=True, projects=True))
- [x] Drive to work (Work) (Away)

```






# Old README

# Todo.txt I/O

A simple Python module to parse, manipulate and write [Todo.txt](http://todotxt.com/) data.

![Python versions](https://img.shields.io/pypi/pyversions/todotxtio.svg?link=https://pypi.python.org/pypi/todotxtio) ![Version](https://img.shields.io/pypi/v/todotxtio.svg?link=https://pypi.python.org/pypi/todotxtio) ![License](https://img.shields.io/pypi/l/todotxtio.svg?link=https://pypi.python.org/pypi/todotxtio?link=https://github.com/EpocDotFr/todotxtio/blob/master/LICENSE.md)

This module tries to comply to the [Todo.txt specifications](https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format) (disclaimer: there aren't any unit tests).

## Documentation

Everything you need to know is located [here](https://epocdotfr.github.io/todotxtio/).

## Changelog

See [here](https://github.com/EpocDotFr/todotxtio/releases).

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/todotxtio/issues).

You can also submit pull requests. It's open-source man!
