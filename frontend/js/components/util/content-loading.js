//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Message, Icon, Image } from "semantic-ui-react";

//IMPORT ASSETS=============================================================
import LoadingImg from "img/loading.gif";

//IMPORT HOOKS==============================================================
import useDelayedLoading from "hooks/delayed-loading";

//COMPONENT=================================================================
function ContentLoading(props) {
    const loadingContent = useDelayedLoading(200);

    function render(){
        if(loadingContent){
            const { type } = props;
            if (type == "message"){
                return (
                    <Message icon info>
                        <Icon name="circle notched" loading />
                        <Message.Content>
                            <Message.Header>Loading</Message.Header>
                            Please wait while loading your content.
                        </Message.Content>
                    </Message>
                )
            }
            else{
                return <Image src={LoadingImg} alt="Loading..." centered />
            }    
        }
        else{
            return null;
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ContentLoading;