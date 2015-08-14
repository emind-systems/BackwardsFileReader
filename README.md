BackwardsFileReader
===================

This repository contains a Python class which reads a file backwards, line by line, while also maintaining the position of the cursor (which is the beginning of the last line read).

The solution was meant to be as efficient as possible, while also keeping the code clear:
 - The algorithm is O(n) in the common scenario where all lines are no longer than a constant value "c".
 - In the extreme case where the file consists mainly of one huge line, the solution is O(n^2), but it still performs better than any other implementation I was able to find on the internet.

Usage example:
```python
bfr = BackwardsFileReader(file)
for line in bfr.read_lines():
    print "(" + str(bfr.current_line_pos) + "): " + line
```
**Note**: This is limited to files written with Unix line endings.

License
-------

See the [LICENSE](LICENSE.md) file for license rights and limitations.
