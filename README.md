# bf2asmjs

A simple brainfuck compiler targeting asm.js.

## Example

```
$ python bf2asmjs.py examples/hello.b > bf.js
$ firefox-trunk index.html
```

## Usage
```
usage: bf2asmjs.py [-h] [--heap HEAP] [--put PUT] [--get GET] file

Compile brainfuck to asm.js.

positional arguments:
  file         brainfuck source file

optional arguments:
  -h, --help   show this help message and exit
  --heap HEAP  number of bytes in the heap, brainfuck usually has at least
               30000
  --put PUT    javascript function implementing .
  --get GET    javascript function implementing ,
```

## Why?

To begin familiarizing myself with targeting asm.js I wanted to create
the simplest possible compiler. I'll admit it's not very useful but
it got me off the ground and it might help others.

## What is asm.js?

Asm.js is a strict subset of javascript meant to be used as a low-level
target for compilers. By virtue of being a subset of javascript it
can be run on javascript engines that do not support its compilation
making it possible to write high performance code that is also backward
compatible. Compiled asm.js modules are fast, performing at around 2x
of native.

## What is brainfuck?

brainfuck is a programming language with a small instruction set and is
designed to be as easy as possible to compile.

```
From Wikipedia

>   increment the data pointer (to point to the next cell to the right).
<   decrement the data pointer (to point to the next cell to the left).
+   increment (increase by one) the byte at the data pointer.
-   decrement (decrease by one) the byte at the data pointer.
.   output the byte at the data pointer.
,   accept one byte of input, storing its value in the byte at the data pointer.
[   if the byte at the data pointer is zero, then instead of moving the
    instruction pointer forward to the next command, jump it forward to the
    command after the matching ] command.
]   if the byte at the data pointer is nonzero, then instead of moving the
    instruction pointer forward to the next command, jump it back to the command
    after the matching [ command.
```

## Heap & Memory.

Asm.js modules use instances of ArrayBuffer as heaps and then create
"views" on them to address data. As brainfucks cells are bytes I use
the Uint8Array view.

## Input & Output

`. ,` is done via the FFI. Default `.` is writing to an element with
id `output`, default `,` is reading from an element with id `input`.
