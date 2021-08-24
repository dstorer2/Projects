using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using ApartmentNetwork.Models;

namespace ApartmentNetwork
{
    public class Post
    {
        [Key]
        public int PostId {get; set; }
        [Required]
        [Display(Name = "Title: ")]
        public string Title {get; set; }
        [Required]
        [Display(Name = "Description: ")]
        public string Description {get; set; }
        public int UserId {get; set; }
        public User Poster {get; set; }
    }
}