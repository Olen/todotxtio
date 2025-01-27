import os
import re
import shutil
from datetime import datetime, date
from collections import UserList

__version__ = '0.3.0'

__all__ = [
    'Todo',
    'TodoList',
]

todo_data_regex = re.compile('^(?:(x) )?(?:(\d{4}-\d{2}-\d{2}) )?(?:\(([A-Z])\) )?(?:(\d{4}-\d{2}-\d{2}) )?')
todo_project_regex = re.compile(' \+(\S+)')
todo_context_regex = re.compile(' @(\S+)')
todo_tag_regex = re.compile(' (\S+):([^\s\/]+)')


class TodoList(UserList):
    def __init__(self, **args):
        self.filename = None

        if 'filename' in args:
            self.filename = args['filename']
            del args['filename']
        super(TodoList, self).__init__(args)
        self.load()

    def replace(self, todo, index = None):
        """Replace existing todo-entry or add a new one.
        """
        if index:
            self.data[index] = todo
        else:
            self.append(todo)

    def load(self):
        if self.filename:
            self.from_file(self.filename)

    def save(self):
        if self.filename:
            self.to_file(self.filename)

    @property
    def sorted(self):
        ret = TodoList()
        for todo in sorted(self, key = lambda i: i.text):
            ret.append(todo)
        return ret

    @property
    def incomplete(self):
        ret = TodoList()
        for todo in self:
            if not todo.completed:
                ret.append(todo)
        return ret

    @property
    def completed(self):
        ret = TodoList()
        for todo in self:
            if todo.completed:
                ret.append(todo)
        return ret

    def projects(self, projects):
        if isinstance(projects, str):
            projects = [projects]
        ret = TodoList()
        for todo in self:
            for p in projects:
                if p in todo.projects and todo not in ret:
                    ret.append(todo)
        return ret

    def contexts(self, contexts):
        if isinstance(contexts, str):
            contexts = [contexts]
        ret = TodoList()
        for todo in self:
            for c in contexts:
                if c in todo.contexts and todo not in ret:
                    ret.append(todo)
        return ret



    def from_dicts(self, todos):
        """Convert a list of todo dicts to a list of :class:`todotxtio.Todo` objects.
    
        :param list todos: A list of todo dicts
        :rtype: list
        """
        return [Todo(**todo) for todo in todos]
    
    
    def from_stream(self, stream, close=True):
        """Load a todo list from an already-opened stream.
    
        :param file stream: A file-like object
        :param bool close: Whetever to close the stream or not after all operation are finised
        :rtype: list
        """
        string = stream.read()
    
        if close:
            stream.close()
    
        self.from_string(string)
    
    
    def from_file(self, file_path, encoding='utf-8'):
        """Load a todo list from a file.
    
        :param str file_path: Path to the file
        :param str encoding: The encoding of the file to open
        :rtype: list
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError('File doesn\'t exists: ' + file_path)
    
        stream = open(file_path, 'r', encoding=encoding)
    
        self.from_stream(stream)
    
    
    def from_string(self, string):
        """Load a todo list from a string.
    
        :param str string: The string to parse
        :rtype: list
        """
        self.data = []
    
        for line in string.strip().splitlines():
            line = line.strip()
    
            todo_pre_data = todo_data_regex.match(line)
    
            todo = Todo()
    
            if todo_pre_data:
                todo.completed = todo_pre_data.group(1) == 'x'
    
                if todo.completed:
                    todo.creation_date = todo_pre_data.group(4)
    
                    if todo_pre_data.group(2):
                        todo.completion_date = todo_pre_data.group(2)
                else:
                    todo.creation_date = todo_pre_data.group(2)
    
                todo.priority = todo_pre_data.group(3)
    
                text = todo_data_regex.sub('', line).strip()
            else:
                text = line
    
            todo_projects = todo_project_regex.findall(text)
    
            if len(todo_projects) > 0:
                todo.projects = todo_projects
                text = todo_project_regex.sub('', text).strip()
    
            todo_contexts = todo_context_regex.findall(text)
    
            if len(todo_contexts) > 0:
                todo.contexts = todo_contexts
                text = todo_context_regex.sub('', text).strip()
    
            todo_tags = todo_tag_regex.findall(text)
    
            if len(todo_tags) > 0:
                for todo_tag in todo_tags:
                    todo.tags[todo_tag[0]] = todo_tag[1]
    
                text = todo_tag_regex.sub('', text).strip()
    
            todo.text = text
            if todo.text:
                self.data.append(todo)
    
        return self.data
    
    
    def to_markdown(self, priority=False, projects=False, contexts=False):
        """Convert a list of :class:`todotxtio.Todo` objects to a markdown checklist.
    
        :param list todos: List of :class:`todotxtio.Todo` objects
        :rtype: string
        """
        return "\n".join([todo.to_markdown(priority=priority, projects=projects, contexts=contexts) for todo in self.data])
    
    
    def to_dicts(self):
        """Convert a list of :class:`todotxtio.Todo` objects to a list of todo dict.
    
        :param list todos: List of :class:`todotxtio.Todo` objects
        :rtype: list
        """
        return [todo.to_dict() for todo in self.data]
    
    
    def to_stream(self, stream, close=True):
        """Write a list of todos to an already-opened stream.
    
        :param file stream: A file-like object
        :param list todos: List of :class:`todotxtio.Todo` objects
        :param bool close: Whetever to close the stream or not after all operation are finised
        :rtype: None
        """
        stream.write(self.to_string())
    
        if close:
            stream.close()
    
    
    def to_file(self, file_path, encoding='utf-8'):
        """Write a list of todos to a file.
    
        :param str file_path: Path to the file
        :param list todos: List of :class:`todotxtio.Todo` objects
        :param str encoding: The encoding of the file to open
        :rtype: None
        """
        if os.path.exists(file_path):
            """ Make a backup before saving the file """
            shutil.copy2(file_path, f"{file_path}.bak")
        stream = open(file_path, 'w', encoding=encoding)
        self.to_stream(stream)
    
    
    def to_string(self):
        """Convert a list of todos to a string.
    
        :param list todos: List of :class:`todotxtio.Todo` objects
        :rtype: str
        """
        return '\n'.join([str(todo) for todo in self.data])

    def search(self, text=None, completed=None, completion_date=None, priority=None, creation_date=None, projects=None, contexts=None, tags=None, exact=None):
        """Return a list of todos that matches the provided filters.
    
        It takes the exact same parameters as the :class:`todotxtio.Todo` object constructor, and return a list of :class:`todotxtio.Todo` objects as well.
        All criteria defaults to ``None`` which means that the criteria is ignored.
    
        A todo will be returned in the results list if all of the criteria matches. From the moment when a todo is sent in the results list, it will
        never be checked again.
    
        :param str text: String to be found in the todo text
        :param bool completed: Search for completed/uncompleted todos only
        :param str completion_date: Match this completion date
        :param list priority: List of priorities to match
        :param str creation_date: Match this creation date
        :param list projects: List of projects to match
        :param list contexts: List of contexts to match
        :param dict tags: Dict of tag to match
        :rtype: list
        """
        results = []
   
        i = 0 
        for todo in self.data:
            text_match = completed_match = completion_date_match = priority_match = creation_date_match = projects_match = contexts_match = tags_match = exact_match = True
    
            if text is not None:
                text_match = text in todo.text
    
            if completed is not None:
                completed_match = todo.completed == completed
    
            if completion_date is not None:
                completion_date_match = todo.completion_date == completion_date
    
            if priority is not None:
                priority_match = todo.priority in priority
    
            if creation_date is not None:
                creation_date_match = todo.creation_date == creation_date
    
            if projects is not None:
                projects_match = any(i in projects for i in todo.projects)
    
            if contexts is not None:
                contexts_match = any(i in contexts for i in todo.contexts)
    
            if tags is not None:
                tags_match = any(todo.tags[k] == v for k, v in tags.items() if k in todo.tags)
    
            if exact is not None:
                exact_match = todo.text == exact
    
            if text_match and completed_match and completion_date_match and priority_match and creation_date_match and projects_match and contexts_match and tags_match and exact_match:
                results.append((i, todo))
            i = i + 1
    
        return results


    def __repr__(self):
        i = 0
        ret = []
        for todo in self.data:
            ret.append((i, todo))
            i = i + 1
        return str(ret)


class Todo:
    """Represent one todo.

    :param str text: The text of the todo
    :param bool completed: Should this todo be marked as completed?
    :param str completion_date: A date of completion, in the ``YYYY-MM-DD`` format. Setting this property will automatically set the ``completed`` attribute to ``True``.
    :param str priority: The priority of the todo represented by a char between ``A-Z``
    :param str creation_date: A date of creation, in the ``YYYY-MM-DD`` format
    :param list projects: A list of projects without leading ``+``
    :param list contexts: A list of projects without leading ``@``
    :param dict tags: A dict of tags
    """
    text = None
    completed = False
    completion_date = None
    priority = None
    creation_date = None
    projects = []
    contexts = []
    tags = {}

    def __init__(self, text=None, completed=False, completion_date=None, priority=None, creation_date=None, projects=None, contexts=None, tags=None):
        self.text = text
        self.completed = completed

        if completion_date and self.completed:
            self.completion_date = completion_date

        self.priority = priority
        self.creation_date = creation_date
        self.projects = projects
        self.contexts = contexts
        self.tags = tags

    def to_dict(self):
        """Return a dict representation of this Todo instance.

        :rtype: dict
        """
        return {
            'text': self.text,
            'completed': self.completed,
            'completion_date': self.completion_date,
            'priority': self.priority,
            'creation_date': self.creation_date,
            'projects': self.projects,
            'contexts': self.contexts,
            'tags': self.tags,
        }

    def to_markdown(self, priority=False, projects=False, contexts=False):
        pre = '- [ ]'
        pri = ''
        pro = ''
        con = ''
        if self.completed:
            pre = '- [x]'
        if priority:
            pri = f" **{self.priority}**"
        if projects and len(self.projects) > 0:
            pro = " (" + ", ".join(self.projects) + ")"
        if contexts and len(self.contexts) > 0:
            con = " (" + ", ".join(self.contexts) + ")"
        return f"{pre} {self.text}{pri}{pro}{con}"

    def __setattr__(self, name, value):
        if name == 'completed':
            if not value:
                super().__setattr__('completion_date', None) # Uncompleted todo must not have any completion date
        elif name == 'creation_date':
            if value:
                if isinstance(value, date) or isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d")
        elif name == 'completion_date':
            if value:
                if isinstance(value, date) or isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d")
                super().__setattr__('completed', True) # Setting the completion date must set this todo as completed...
            else:
                super().__setattr__('completed', False) # ...and vice-versa
        elif name in ['projects', 'contexts']:
            if not value:
                super().__setattr__(name, []) # Force contexts, projects to be lists when setting them to a falsely value
                return
            elif type(value) is not list: # Make sure, otherwise, that the provided value is a list
                raise ValueError(name + ' should be a list')
        elif name == 'tags':
            if not value:
                super().__setattr__(name, {}) # Force tags to be a dict when setting them to a falsely value
                return
            elif type(value) is not dict: # Make sure, otherwise, that the provided value is a dict
                raise ValueError(name + ' should be a dict')

        super().__setattr__(name, value)

    def __str__(self):
        """Convert this Todo object in a valid Todo.txt line."""
        ret = []

        if self.completed:
            ret.append('x')

        if self.completion_date:
            ret.append(self.completion_date)

        if self.priority:
            ret.append('(' + self.priority + ')')

        if self.creation_date:
            ret.append(self.creation_date)

        ret.append(self.text)

        if self.projects:
            ret.append(''.join([' +' + project for project in set(self.projects)]).strip())

        if self.contexts:
            ret.append(''.join([' @' + context for context in set(self.contexts)]).strip())

        if self.tags:
            ret.append(''.join([' ' + tag_name + ':' + tag_value for tag_name, tag_value in self.tags.items()]).strip())

        return ' '.join(ret)

    def __repr__(self):
        """Call the __str__ method to return a textual representation of this Todo object."""
        return self.__str__()


