import logging

class ExtraRecordsFormatter(logging.Formatter):
    """A Formatter that adds a few items to the record:

    filenameandlineno
        a combination of filename:linenumber so they can be justified together
    
    shortfuncname
        the function name truncated and left justified to 15 characters. You
        can change the length by setting the funcLength property

    shortlevelname
        the levelname truncated to 1 character. Useful for very compact log
        messages

    """
    funcLength = 15

    def format(self, record):
        record.filenameandlineno = "{}:{}".format(record.filename, record.lineno)

        record.shortfuncname = "{0:<{length}}".format(record.funcName[:self.funcLength], length=self.funcLength)

        record.shortlevelname = record.levelname[0]

        return super().format(record)


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
class UnixColorFormatter(logging.Formatter):
    """A formatter meant for output to a linux console.
    The following colors are added to the following fields:

    * colorlevelname is colored blue for debug, orange for warning,
      and highlighted red for error and above
    * The entire message is also highlighted red for error and above

    You can change the class variables COLORIZE and HIGHLIGHT to change the
    colors and levels used, but *what's* colored is hard coded: the levelname
    field for colors or the entire message for highlights.

    format specifications must be in the string.format '{' style.

    """
    COLORIZE = {
        'DEBUG': CYAN,
        'INFO': WHITE,
    }
    HIGHLIGHT = {
        'CRITICAL': RED,
        'ERROR': RED,
        'WARNING': YELLOW,
    }


    def __init__(self, levelname_format, **kwargs):
        """Because the color codes take up room in the strings, the levelname
        field must be justified before color is applied. the levelname_format
        parameter should be a string containing the format you wish to use. For
        example, levelname_format="{:<8}"

        """
        # Hard wired for this format style
        kwargs['style'] = "{"
        self.levelname_format = levelname_format

        super().__init__(**kwargs)

    def format(self, record):

        # Justify the levelname filed here before it's colorized
        origlevelname = record.levelname
        adjustedlevelname = self.levelname_format.format(record.levelname)


        # Add color to the levelname field as configured depending on the level
        if origlevelname in self.COLORIZE:
            newlevelname = "{color}{record}{reset}".format(
                    color = COLOR_SEQ % (30 + self.COLORIZE[origlevelname]),
                    record = adjustedlevelname,
                    reset = RESET_SEQ,
                    )
            record.colorlevelname = newlevelname
        else:
            record.colorlevelname = origlevelname

        # Format the record here
        line = super().format(record)

        # Highlight the entire entry as configured depending on the level
        if origlevelname in self.HIGHLIGHT:
            # Highlight the entire line
            color = COLOR_SEQ % (40 + self.HIGHLIGHT[origlevelname])
            # Allows for other color in the string. When that's reset, re-apply
            # our highlight.
            line = line.replace(RESET_SEQ, RESET_SEQ+color)
            
            line = "{color}{line}{reset}".format(
                    color = color,
                    line = line,
                    reset = RESET_SEQ,
                    )

        return line

