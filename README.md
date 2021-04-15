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

todo = Todo(text="Something to do")
todo.contexts.append('Home')
print(todo.to_dict())

# Add the entry to the list

todolist.append(todo)

print(todolist)

# You can also add some magic functions to the lists

print(todolist.to_markdown())
# - [ ] Something to do

print(todolist.to_markdown(contexts=True))
# - [ ] Something to do (Home)

# And also some inline search and filtering:

print(todolist.contexts(['Home', 'Away']).incomplete.sorted.to_markdown(projects=True))
# - [ ] Answer the phone (Work)
# - [ ] Buy groceries (Shopping, Dinner)
# - [ ] Complete README (Todotxtio)
# - [ ] Drive to work (Work)


# Change an entry in the todolist:

searchresult = todolist.search(exact="Drive to work")
index, todo = searchresult[0]
todo.completed = True
todolist.replace(todo, index)

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
