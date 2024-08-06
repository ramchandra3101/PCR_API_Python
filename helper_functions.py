import System
def call_csharp_method(obj, method_name, *args):
    try:
        # Get the Type of the object
        obj_type = obj.GetType()
        
        # Try to find the method
        method = obj_type.GetMethod(method_name)
        
        if method is None:
            print(f"Method '{method_name}' not found. Available methods:")
            for m in obj_type.GetMethods():
                print(f"  {m.Name}")
            return None

        # If we found the method, invoke it
        return method.Invoke(obj, args)

    except system.Reflection.TargetInvocationException as tie:
        inner_exception = tie.InnerException
        print(f"C# method '{method_name}' threw an exception: {inner_exception}")
        print(f"C# stack trace: {inner_exception.StackTrace}")
        return None
    except Exception as e:
        print(f"Error calling C# method '{method_name}': {str(e)}")
        return None  