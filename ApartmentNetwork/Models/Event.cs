using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using ApartmentNetwork.Models;

namespace ApartmentNetwork
{
    public class Event : Post
    {
        [Required]
        [Display(Name = "Date and time of Event: ")]
        public DateTime EventDate {get; set; }
        [Required]
        [Display(Name = "Location of Event: ")]
        public string Location {get; set; }
    }
}