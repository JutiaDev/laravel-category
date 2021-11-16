<?php

namespace JutiaDev\Category\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Categorizable extends Model
{
    use HasFactory;

    public const TABLE_NAME = 'categorizables';

    public const CATEGORY_ID = 'category_id';
    public const CATEGORIZABLE_ID = 'categorizable_id';
    public const CATEGORIZABLE_TYPE = 'categorizable_type';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    public $fillable = [
        self::CATEGORY_ID,
        self::CATEGORIZABLE_ID,
        self::CATEGORIZABLE_TYPE,
    ];

    public function getTable()
    {
        return self::TABLE_NAME;
    }

}
