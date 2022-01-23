I don't have a name for this yet
---
A basic stack based language

Constants:
    The `const` keyword at the top of the program is used to define constants as a literal (see below), constants are used during __translation__ to replace later values in code.
    Constants must not include spaces, share a name with a keyword or another constant - if more than one constant has the same name, the latest one will be used.
    Constants cannot be changed.

Literals:
    A string or integer [ TODO: ADD FLOAT SUPPORT ] literal will just be pushed to the stack.
    A string literal is *any* text between "" or ''.
    An integer literal is just a number.
    Literals are seperated by spaces.
    `inpi` - Take in an integer from the user
    `inps` - Take in a string from the user

Stack Control:
    `copy` - Copies the top element of the stack.
    `drop` - Removes the top element of the stack.
    `print`- Prints, and removes, the top element of the stack.
    `swap` - Swaps the top two elements of the stack.
    `clear`- Empties the stack.

Flow Control:
    `if`   - Removes the top element of the stack, if it is True it runs the following code, else it jumps to its associated `end`.
    `for`  - Followed by `n->m` where n and m are integer literals, repeats the following block of code, pushing the next number between n and m inclusive to the stack each time.
    `while`- Removes the top element of the stack, if True run the following code; repeat once hitting end.
             Removes an element from the stack *every* repeat, including final False value.
    `end`  - Marks the end of a code block.

Boolean Logic:
    Note: an non-zero integer; a non-empty string; or True are classified as a boolean true, everything else is a boolean false.
    `not`  - Removes the top element of the stack, and pushes the opposite boolean value.
    `and`  - Removes the top two elements of the stack, and pushes the result of a logical and.
    `or`   - Removes the top two elements of the stack, and pushes the result of a logical or.
