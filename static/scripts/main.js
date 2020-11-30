function validation(){

    if(document.tournament.name.value == "" || document.tournament.name.value.length < 3) {
        alert("Preencha o campo nome corretamente (mínimo 3 caracteres).");
        document.tournament.name.focus;
        return false;
    }

    n = document.getElementById("competitors_number").value;
    if (n && (n & (n - 1)) != 0 || n == 1) {
        alert("Preencha o campo de número de competidores com uma potência de 2).");
        return false;
    }
}

function validatecompetitor(){

    if(document.competitor.name.value == "" || document.competitor.name.value.length < 3) {
        alert("Preencha o campo nome corretamente (mínimo 3 caracteres).");
        document.competitor.name.focus;
        return false;
    }
}

/*function  power_of_2(){

    n = document.tournament.competitors_number.value;
    alert(n);

    if (n && (n & (n - 1))) != 0 {
        alert("Preencha o campo de número de competidores com uma potência de 2).");
        document.tournament.competitors_number.focus;
        return false;
    }
}*/