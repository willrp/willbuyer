//IMPORT EXTERNAL COMPONENTS================================================
import { useState, useEffect } from "react";

//HOOK======================================================================
function useIsPhone() {
    const [isPhone, setIsPhone] = useState(false);

    function handleResize() {
        if(window.innerWidth <= 600){
            setIsPhone(true);
        }
        else{
            setIsPhone(false);
        }
    }

    useEffect(() => {
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, [])

    return isPhone;
}

//EXPORT HOOK===============================================================
export default useIsPhone;