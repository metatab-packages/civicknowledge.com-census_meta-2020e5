""" Example pylib functions"""



def custom_update(doc, args):
    """Custom update function, run with `mp update -U`

    The args argument will recieve any remainder arguments from the call, for instance

        mp update -U -- --foo bar

    """

    doc.reference('source')

    doc.write()
