using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using ApartmentNetwork.Models;

namespace ApartmentNetwork
{
    public class Address
    {
        [Key]
        public int AddressId {get; set; }
        [Required]
        public string AddressLine1 {get; set; }
        [Required]
        public string City {get; set; }
        [Required]
        public string State {get; set; }
        [Required]
        public int ZipCode {get; set; }
        public DateTime CreatedAt {get; set; } = DateTime.Now;
        public DateTime UpdatedAt {get; set; } = DateTime.Now;
        public int BuildingId {get; set; }
        public Building Building {get; set; }

    }
}