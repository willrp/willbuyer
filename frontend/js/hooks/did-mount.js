//IMPORT EXTERNAL COMPONENTS================================================
import { useRef, useEffect } from "react";

//HOOK======================================================================
function useDidMount() {
    const didMount = useRef(true);

    useEffect(() => {
        didMount.current = false;
    }, [])

    return didMount.current;
}

//EXPORT HOOK===============================================================
export default useDidMount;