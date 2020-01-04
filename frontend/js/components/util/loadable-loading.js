//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Image } from "semantic-ui-react";

//IMPORT ASSETS=============================================================
import LoadingImg from "img/loading.gif";

//IMPORT HOOKS==============================================================
import useDelayedLoading from "hooks/delayed-loading";

//COMPONENT=================================================================
function LoadableLoading() {
    const loadingContent = useDelayedLoading(200);

    function render(){
        if(loadingContent){
            return <Image src={LoadingImg} alt="Loading..." centered />
        }
        else{
            return null;
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default LoadableLoading;