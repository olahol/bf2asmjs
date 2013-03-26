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
GET = """function () { return prompt("one char").charCodeAt(0) || 0; }"""

CODE = """
;(function (ctx) {
    function BF(stdlib, ffi, heap) {
        "use asm";

        var m = new stdlib.Uint8Array(heap);
        var p = 0;
        var put = ffi.put;
        var get = ffi.get;

        function run() { %s }

        function reset(b) {
            b = b|0;
            var i = 0;
            while ((i|0) < (b|0)) {
                m[i] = 0;
                i = (i + 1)|0;
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
    return CODE % (ins, name, put, get, heapsize)

if __name__ == "__main__":
    import sys, os

    """
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')
    args = parser.parse_args()
    """

    file = sys.argv[1]
    name = os.path.basename(os.path.splitext(file)[0])
    src = open(file).read()

    print compile(name, src)
