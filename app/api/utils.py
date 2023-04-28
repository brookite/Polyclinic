from flask import jsonify

def require_arguments(reqargs, *args):
    result = {}
    missing = []
    for arg in args:
        if arg in reqargs:
            result[arg] = reqargs[arg]
        else:
            missing.append(arg)
    return result, missing


def missing_arguments(*args):
    args = ", ".join(args)
    return jsonify({"error_msg": f"Missing arguments: {args}"})