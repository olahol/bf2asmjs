INS = {
    ">": "p = (p + 1)|0;"
    , "<": "p = (p - 1)|0;"
    , "+": "m[p] = ((m[p]|0) + 1);"
    , "-": "m[p] = ((m[p]|0) - 1);"
    , ".": "put(m[p]|0);"
    , ",": "m[p] = get()|0;"
    , "[": "while ((m[p]|0) > 0) {"
    , "]": "};"
}

PUT = """function (i) { document.getElementById("output").innerHTML += String.fromCharCode(i); }"""
GET = """function () {
    var c = document.getElementById("input").value.charCodeAt(inputPtr) || 0;
    inputPtr++;
    return c;
}"""

CODE = """
;(function (ctx) {
    function BF(stdlib, ffi, heap) {
        "use asm";

        var m = new stdlib.Uint8Array(heap);
        var p = 0;
        var put = ffi.put;
        var get = ffi.get;

        function run() { %s }

        function reset() {
            var i = 0;
            while ((i|0) < (%d|0)) {
                m[i] = 0;
                i = (i + 1)|0
            }
        }

        return { reset: reset, run: run };
    }

    ctx["BF%s"] = BF(ctx, {
        put: %s
        , get: %s
    }, new ArrayBuffer(%d));
})(this)
"""

def compile(name, src, put = PUT, get = GET, heapsize = 4096):
    ins = " ".join([ INS.get(c, "") for c in src ])
    return CODE % (ins, heapsize, name, put, get, heapsize)

if __name__ == "__main__":
    import sys, os, argparse

    parser = argparse.ArgumentParser(description="Compile brainfuck to asm.js.")
    parser.add_argument("file", type=str, help="brainfuck source file")
    parser.add_argument("--heap", default=2**19, type=int, help="number of bytes in the heap, brainfuck usually has at least 30000")
    parser.add_argument("--put", default=PUT, type=str, help="javascript function implementing .")
    parser.add_argument("--get", default=GET, type=str, help="javascript function implementing ,")
    args = parser.parse_args()

    file = args.file
    name = os.path.basename(os.path.splitext(file)[0])
    src = open(file).read()

    print compile(name, src, args.put, args.get, args.heap)
