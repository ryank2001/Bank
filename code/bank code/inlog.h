#include <Arduino.h>

class gebruiker
{
    private:
        String IBAN;
        String pincode;
        String naam;
        int saldo;
        int opnamehoeveelheid;
        int pincodepogingen = 3;

    public:
        gebruiker(){
            this -> pincode = "";
        }


    void clearuser(){
        this->IBAN = "";
        this->pincode= "";
        this->naam = "";
        this->saldo = 0;
        this->opnamehoeveelheid = 0;
    }

    void clearpin(){
        this->pincode = "";
    }

    int opnemenBedrag(){
        return 1;
    }
    int checkpin(){
        if (this->pincode == "1111"){
            return 1;
        }
        return 0;//////moet een check systeem komen!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    }

    int set_iban(String iban){
        if (iban == ""){
            return 0;
        }
        this->IBAN = iban;
        return 1;
    }

    int add_number_pincode(char number){
        this->pincode.concat(number);
        
        return 1;
        
    }

    int set_name(String name){
         if (name == ""){
            return 0;
        }
        this->naam = name;
        return 1;
    }

    int set_saldo(){
        this->saldo = 100;
        return 1;
    }

    int set_opnamehoeveelheid(int hoeveelheid){
        if(hoeveelheid > this->saldo){
            return 0;
        }
        this->opnamehoeveelheid = hoeveelheid;
        return 1;
    }

    String getIBAN(){
        return this->IBAN;
    }

    String  getPincode(){
        return this->pincode;
    }
    
    String getNaam(){
        return this->naam;
    }

    int getSaldo(){
        return this->saldo;
    }

    int getopname(){
        return this->opnamehoeveelheid;
    }

    int getPogingen(){
        return this->pincodepogingen;
    }

    void reducePogingen(){
        pincodepogingen--;
    }

    void seetpincodepogingen(int pogingen){
        this->pincodepogingen = pogingen;
    }



};