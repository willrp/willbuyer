//IMPORT EXTERNAL COMPONENTS================================================
import { useEffect, useState } from "react";

//HOOK======================================================================
function useDelayedLoading(delay) {
    const [delayedLoading, setDelayedLoading] = useState(false);

    useEffect(() => {
        let timeout = null;
        timeout = setTimeout(() => {
            setDelayedLoading(true);
        }, delay)

        return () => {
            clearTimeout(timeout);
        }
    }, [])

    return delayedLoading;
}

//EXPORT HOOK===============================================================
export default useDelayedLoading;