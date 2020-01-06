//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Segment, Responsive } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NotFound from "components/util/not-found";
import Gallery from "./gallery";
import ProductInfo from "./product-info";
import ProductPrice from "./product-price";
import ProductCart from "./product-cart";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const renderClass = css({
    "&&&&&>.segment": {
        width: "50%"
    }
})

//COMPONENT=================================================================
function Product() {
    const { productid } = useParams();
    const [stacked, setStacked] = useState(false);    
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        setRequest({
            url: `/api/store/product/${productid}`,
            method: "get",
            responseType: "json"
        })
    }, [productid])

    useEffect(() => {
        const { status, error } = requestData;
        if(status >= 500 && error !== null){
            throw {status, error};
        }
    }, [requestData])

    function onWidthUpdate() {
        if(window.innerWidth >= Responsive.onlyTablet.minWidth) {
            setStacked(false);
        }
        else {
            setStacked(true);
        }
    }

    function render() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else if(status === 404) {
            return <NotFound />
        }
        else {
            const { images, price } = data;
            return (
                <Responsive 
                    as={Segment.Group}
                    onUpdate={onWidthUpdate}
                    horizontal={!stacked}
                    className={(!stacked) ? renderClass : null}
                    fireOnMount
                >
                    <Segment basic>
                        <Gallery images={images} />
                    </Segment>
                    <Segment basic>
                        <ProductInfo {...data} />
                        <ProductPrice {...price} />
                        <ProductCart productid={productid} />
                    </Segment>
                </Responsive>
            )
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Product;