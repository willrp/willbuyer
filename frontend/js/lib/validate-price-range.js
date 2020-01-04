function validatePriceRange(pricerange) {
    const min = parseInt(pricerange.min);
    const max = parseInt(pricerange.max);

    if(isNaN(min) || min <= 0){
        return null;
    }
    else if(isNaN(max) || max <= 0){
        return null;
    }
    else if(max < min){
        return null;
    }
    else{
        return {min, max};
    }
}

export default validatePriceRange;