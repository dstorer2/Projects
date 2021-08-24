using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using ApartmentNetwork.Models;

namespace ApartmentNetwork
{
    public class Building
    {
        [Key]
        public int BuildingId {get; set; }
        [Required]
        [Display(Name = "Building Name: ")]
        public string BuildingName {get; set; }
        public int AddressId {get; set; }

        public DateTime CreatedAt {get; set; } = DateTime.Now;
        public DateTime UpdatedAt {get; set; } = DateTime.Now;
        public Address Address {get; set; }
        public int UserId {get; set; }
        public User Admin {get; set; }
        public List<User> Residents {get; set; }
    }
}