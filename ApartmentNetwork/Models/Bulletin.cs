using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using ApartmentNetwork.Models;

namespace ApartmentNetwork
{
    public class Bulletin : Post
    {
        [Required]
        [Display(Name = "Topic of Bulletin: ")]
        public string Topic {get; set; }
    }
}